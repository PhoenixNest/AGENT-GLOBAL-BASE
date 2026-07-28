"""Fake chat models for offline verification -- no API key available in this environment.

Deliberately duplicated from supporting/enterprise-examples/ rather than imported from it: this
project must stand on its own, per the CEO-approved boundary between workspace-integration-examples/
and enterprise-examples/.
"""

from langchain_core.language_models.fake_chat_models import FakeListChatModel


class ToolCapableFakeChatModel(FakeListChatModel):
    """FakeListChatModel does not implement bind_tools, and create_agent / create_deep_agent
    call model.bind_tools(...) unconditionally -- even when no caller-supplied tools exist,
    because DeepAgents always registers its own built-in tools. Without this override,
    building any agent against a fake model raises NotImplementedError before a single
    message is ever sent.
    """

    def bind_tools(self, tools, **kwargs):
        return self
