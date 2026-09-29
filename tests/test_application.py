import io

from web.app import app, transfers, audit_log


def setup_function():
    """Reset in-memory application state before each test."""
    transfers.clear()
    audit_log.clear()


def test_home_redirects_to_receiver():
    """Verify the home route redirects to the receiver page."""
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 302
    assert response.location.endswith("/receiver")


def test_sender_page_loads():
    """Verify the sender interface is available."""
    client = app.test_client()

    response = client.get("/sender")

    assert response.status_code == 200
    assert b"Sender" in response.data or b"sender" in response.data


def test_receiver_page_loads():
    """Verify the receiver interface is available."""
    client = app.test_client()

    response = client.get("/receiver")

    assert response.status_code == 200
    assert b"Receiver" in response.data or b"receiver" in response.data


def test_receiver_can_generate_rsa_keys():
    """Verify receiver initialization creates a transfer and RSA public key."""
    client = app.test_client()

    response = client.post("/api/receiver/init-transfer")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["transfer_id"]
    assert data["public_key"]
    assert "BEGIN PUBLIC KEY" in data["public_key"]


def test_end_to_end_secure_file_transfer():
    """
    Integration test:
    1. Receiver generates RSA keys.
    2. Sender uploads a file with the receiver's public key.
    3. Application encrypts and transfers the file.
    4. Receiver decrypts the file.
    5. Integrity is verified.
    """
    client = app.test_client()

    # Step 1: Receiver initializes a transfer
    init_response = client.post("/api/receiver/init-transfer")

    assert init_response.status_code == 200

    init_data = init_response.get_json()

    transfer_id = init_data["transfer_id"]
    public_key = init_data["public_key"]

    # Step 2: Sender uploads a file
    original_content = b"CA-II DevOps secure transfer test file."

    encrypt_response = client.post(
        "/api/sender/encrypt",
        data={
            "transfer_id": transfer_id,
            "public_key": public_key,
            "file": (io.BytesIO(original_content), "ca2-test.txt"),
        },
        content_type="multipart/form-data",
    )

    assert encrypt_response.status_code == 200

    encrypt_data = encrypt_response.get_json()

    assert encrypt_data["success"] is True
    assert encrypt_data["transfer_integrity"] is True
    assert encrypt_data["original_name"] == "ca2-test.txt"

    # Step 3: Receiver decrypts the transferred file
    decrypt_response = client.post(
        "/api/receiver/decrypt",
        json={"transfer_id": transfer_id},
    )

    assert decrypt_response.status_code == 200

    decrypt_data = decrypt_response.get_json()

    assert decrypt_data["success"] is True
    assert decrypt_data["integrity_verified"] is True
    assert decrypt_data["original_name"] == "ca2-test.txt"

    # Step 4: Download and verify original content
    download_response = client.get(
        f"/api/receiver/download/{transfer_id}"
    )

    assert download_response.status_code == 200
    assert download_response.data == original_content


def test_invalid_transfer_id_is_rejected():
    """Verify that an unknown transfer ID is rejected."""
    client = app.test_client()

    response = client.post(
        "/api/receiver/check",
        json={"transfer_id": "INVALID1"},
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["success"] is False