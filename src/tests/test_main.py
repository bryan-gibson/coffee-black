# tests/test_main.py

from coffee_bot.main import MESSAGE_FILE, get_twilio_client, get_messages, save_queue_state, load_queue_state, initialize_message_queue
import os
import pytest
import json

@pytest.mark.get_twilio_client
def test_cannot_get_twilio_client(monkeypatch):
    def mock_client_raises(account_sid, auth_token):
        raise Exception("Simulated failure")

    monkeypatch.setattr("coffee_bot.main.Client", mock_client_raises)

    with pytest.raises(Exception, match="Simulated failure"):
        get_twilio_client("fake_sid", "fake_token")

@pytest.mark.get_twilio_client
def test_can_get_twilio_client(monkeypatch):
    class MockClient:
        def __init__(self, account_sid, auth_token):
            self.account_sid = account_sid
            self.auth_token = auth_token

    monkeypatch.setattr("coffee_bot.main.Client", MockClient)

    client = get_twilio_client("fake_sid", "fake_token")

    assert client is not None
    assert client.account_sid == "fake_sid"
    assert client.auth_token == "fake_token"

@pytest.mark.get_messages
def test_get_messages_file_not_found(tmp_path, monkeypatch):       
    monkeypatch.chdir(tmp_path)    
    result = get_messages()
    
    assert result is None, \
        f"Expected None, but got {result}"

@pytest.mark.get_messages
def test_can_get_messages(tmp_path, monkeypatch):
    messages_file = "coffee_messages.json"  
    file_path = tmp_path / messages_file
    messages = {
        "message1": "Hello",
        "message2": "World"
    }
    file_path.write_text(json.dumps(messages))
    
    monkeypatch.chdir(tmp_path)
    
    result1 = get_messages(file_name=messages_file)
    assert result1 == messages

@pytest.mark.save_queue_state
def test_save_queue_state(tmp_path):
    queue = {
        "message1": "Hello",
        "message2": "World"
    }
    file_path = tmp_path / "queue.json"
    save_queue_state(queue, file_name=file_path)
    assert file_path.exists(), \
        f"Expected {file_path} to exist, but it does not."
    
@pytest.mark.load_queue_state
def test_load_queue_state_failed(tmp_path):
    file_path = tmp_path / "non_existent_file.json"
    result = load_queue_state(file_name=file_path)
    
    assert result is None, \
        f"Expected None, but got {result}"

@pytest.mark.load_queue_state
def test_load_queue_state(tmp_path):
    queue = {
        "message1": "Hello",
        "message2": "World"
    }
    file_path = tmp_path / "queue.json"
    file_path.write_text(json.dumps(queue))
    
    result = load_queue_state(file_name=file_path)
    assert result == queue, \
        f"Expected {result} to be equal to {queue}, but it is not."
    
@pytest.mark.initialize_message_queue
def test_initialize_message_queue_from_state(tmp_path):
    queue = {
        "message1": "Hello",
        "message2": "World"
    }
    file_path = tmp_path / "queue.json"
    file_path.write_text(json.dumps(queue))
    
    result = initialize_message_queue(file_path)
    
    assert result == queue, \
        f"Expected {result} to be equal to {queue}, but it is not."
    
@pytest.mark.initialize_message_queue
def test_initialize_message_queue_reset(tmp_path, monkeypatch):

    result = initialize_message_queue()

    # check if the queue is equal length to MESSAGE_FILE since it is shuffled
    with open(MESSAGE_FILE, "r") as file:
        messages = json.load(file)
    assert len(result) == len(messages), \
        f"Expected length of result {len(result)} to be equal to length of messages {len(messages)}, but it is not."