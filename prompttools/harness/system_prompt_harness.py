# Copyright (c) Hegel AI, Inc.
# All rights reserved.
#
# This source code's license can be found in the
# LICENSE file in the root directory of this source tree.

from typing import Dict, List, Optional
from prompttools.harness.harness import ExperimentationHarness
from prompttools.experiment.openai_chat_experiment import OpenAIChatExperiment


class SystemPromptExperimentationHarness(ExperimentationHarness):
    r"""
    An experimentation harness used for system prompts.
    """

    PIVOT_COLUMNS = ["system_prompt", "user_input"]

    def __init__(
        self,
        model_name: str,
        system_prompts: List[str],
        human_messages: List[str],
        use_scribe: bool = False,
        scribe_name: str = "System Prompt Experiment",
        model_arguments: Optional[Dict[str, object]] = {},
    ):
        self.experiment_classname = OpenAIChatExperiment
        self.model_name = model_name
        self.system_prompts = system_prompts
        self.human_messages = human_messages
        self.use_scribe = use_scribe
        self.scribe_name = scribe_name
        self.model_arguments = model_arguments
        super().__init__()

    @staticmethod
    def _create_system_prompt(content: str) -> Dict[str, str]:
        return {"role": "system", "content": content}

    @staticmethod
    def _create_human_message(content: str) -> Dict[str, str]:
        return {"role": "user", "content": content}

    def prepare(self) -> None:
        r"""
        Creates messages to use for the experiment, and then initializes and prepares the experiment.
        """
        self.input_pairs_dict = {}
        messages_to_try = []
        for system_prompt in self.system_prompts:
            for message in self.human_messages:
                history = [
                    self._create_system_prompt(system_prompt),
                    self._create_human_message(message),
                ]
                messages_to_try.append(history)
                self.input_pairs_dict[str(history)] = (system_prompt, message)
        self.experiment = self.experiment_classname(
            [self.model_name],
            messages_to_try,
            self.use_scribe,
            self.scribe_name,
            **self._prepare_arguments(self.model_arguments),
        )
        super().prepare()

    def run(self):
        if not self.experiment:
            self.prepare()
        super().run()
