"""Phase 65.2 TASK 1 — voice/stt/models.py: STTRequest/STTResult/STTResultStatus."""

from ai_layer.voice_ai.stt.models import STTRequest, STTResult, STTResultStatus


def test_stt_result_status_has_three_values():
    assert {s.value for s in STTResultStatus} == {"PENDING", "READY", "REJECTED"}


def test_stt_request_defaults():
    request = STTRequest(id="r1", audio=b"AUDIO")
    assert request.language == "en"
    assert request.requested_at == ""


def test_stt_request_is_frozen():
    request = STTRequest(id="r1", audio=b"AUDIO")
    try:
        request.language = "fr"
        assert False, "STTRequest should be frozen"
    except AttributeError:
        pass


def test_stt_result_defaults():
    result = STTResult(request_id="r1", status=STTResultStatus.PENDING)
    assert result.text is None
    assert result.reason == ""
    assert result.generated_at == ""
    assert result.metadata == {}


def test_stt_result_is_frozen():
    result = STTResult(request_id="r1", status=STTResultStatus.PENDING)
    try:
        result.status = STTResultStatus.READY
        assert False, "STTResult should be frozen"
    except AttributeError:
        pass


def test_stt_result_ready_carries_text():
    result = STTResult(request_id="r1", status=STTResultStatus.READY, text="hello gold")
    assert result.text == "hello gold"
