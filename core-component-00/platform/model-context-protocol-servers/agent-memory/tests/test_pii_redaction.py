"""
Unit tests for pii_redaction.py in isolation from write_tool.py's
integration (see test_write_memory.py's TestPiiRedactionBeforeEmbed for the
"actually happens before embedding" integration coverage; see
pii_redaction.py's own module docstring for what it redacts and why).
"""
import sys
from pathlib import Path

_AGENT_MEMORY_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_AGENT_MEMORY_DIR))

from pii_redaction import redact_pii  # noqa: E402


class TestEmailRedaction:
    def test_simple_email_redacted(self):
        assert redact_pii("contact jane.doe@example.com now") == "contact [REDACTED_EMAIL] now"

    def test_plus_addressed_email_redacted(self):
        result = redact_pii("send to alerts+prod@sub.example.co.uk")
        assert "alerts+prod@sub.example.co.uk" not in result
        assert "[REDACTED_EMAIL]" in result

    def test_multiple_emails_all_redacted(self):
        result = redact_pii("cc a@x.com and b@y.com")
        assert "a@x.com" not in result
        assert "b@y.com" not in result
        assert result.count("[REDACTED_EMAIL]") == 2


class TestPhoneRedaction:
    def test_dashed_format_redacted(self):
        result = redact_pii("call 555-123-4567 today")
        assert "555-123-4567" not in result
        assert "[REDACTED_PHONE]" in result

    def test_parenthesized_area_code_redacted(self):
        result = redact_pii("reach me at (555) 123-4567 anytime")
        assert "(555) 123-4567" not in result
        assert "[REDACTED_PHONE]" in result

    def test_dotted_format_redacted(self):
        result = redact_pii("phone: 555.123.4567")
        assert "555.123.4567" not in result
        assert "[REDACTED_PHONE]" in result

    def test_plain_digits_redacted(self):
        result = redact_pii("number is 5551234567 apparently")
        assert "5551234567" not in result
        assert "[REDACTED_PHONE]" in result

    def test_country_code_prefixed_redacted(self):
        result = redact_pii("dial +1-555-123-4567 for support")
        assert "555-123-4567" not in result
        assert "[REDACTED_PHONE]" in result


class TestSsnRedaction:
    def test_standard_ssn_format_redacted(self):
        result = redact_pii("SSN on file: 123-45-6789")
        assert "123-45-6789" not in result
        assert "[REDACTED_SSN]" in result

    def test_bare_nine_digit_run_not_treated_as_ssn(self):
        """Deliberate scope limit (see pii_redaction.py docstring): a bare
        9-digit run with no SSN-style dashes is not redacted as SSN — too
        many ordinary numeric identifiers would false-positive."""
        result = redact_pii("order number 123456789 confirmed")
        assert result == "order number 123456789 confirmed"


class TestCreditCardRedaction:
    def test_spaced_16_digit_card_redacted(self):
        result = redact_pii("card 4111 1111 1111 1111 on file")
        assert "4111 1111 1111 1111" not in result
        assert "[REDACTED_CC]" in result

    def test_dashed_16_digit_card_redacted(self):
        result = redact_pii("card 4111-1111-1111-1111 on file")
        assert "4111-1111-1111-1111" not in result
        assert "[REDACTED_CC]" in result

    def test_unspaced_16_digit_card_redacted(self):
        result = redact_pii("card 4111111111111111 on file")
        assert "4111111111111111" not in result
        assert "[REDACTED_CC]" in result

    def test_amex_15_digit_card_redacted(self):
        result = redact_pii("amex 378282246310005 on file")
        assert "378282246310005" not in result
        assert "[REDACTED_CC]" in result

    def test_ten_digit_phone_number_not_treated_as_credit_card(self):
        result = redact_pii("call 5551234567 please")
        assert "[REDACTED_PHONE]" in result
        assert "[REDACTED_CC]" not in result


class TestMixedAndEdgeCases:
    def test_multiple_pii_classes_in_one_string_all_redacted(self):
        result = redact_pii(
            "Jane's email is jane@example.com, SSN 123-45-6789, "
            "card 4111 1111 1111 1111, phone 555-123-4567."
        )
        assert "jane@example.com" not in result
        assert "123-45-6789" not in result
        assert "4111 1111 1111 1111" not in result
        assert "555-123-4567" not in result
        assert "[REDACTED_EMAIL]" in result
        assert "[REDACTED_SSN]" in result
        assert "[REDACTED_CC]" in result
        assert "[REDACTED_PHONE]" in result

    def test_no_pii_returns_input_unchanged(self):
        plain = "the deploy window moved to Thursday afternoon"
        assert redact_pii(plain) == plain

    def test_empty_string_returned_unchanged(self):
        assert redact_pii("") == ""

    def test_none_input_returned_unchanged_never_raises(self):
        assert redact_pii(None) is None

    def test_non_string_input_returned_unchanged_never_raises(self):
        assert redact_pii(12345) == 12345

    def test_result_is_a_new_string_type_preserved(self):
        result = redact_pii("no pii here")
        assert isinstance(result, str)
