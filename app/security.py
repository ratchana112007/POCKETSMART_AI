import base64
import hashlib
import hmac
import secrets


ALGORITHM = "sha256"

ITERATIONS = 310_000


def hash_password(password: str) -> str:

    salt = secrets.token_bytes(16)

    digest = hashlib.pbkdf2_hmac(
        ALGORITHM,
        password.encode(),
        salt,
        ITERATIONS
    )

    return (
        f"pbkdf2_{ALGORITHM}"
        f"${ITERATIONS}"
        f"${base64.urlsafe_b64encode(salt).decode()}"
        f"${base64.urlsafe_b64encode(digest).decode()}"
    )


def verify_password(
    password: str,
    encoded: str
) -> bool:

    try:

        _,
        algorithm,
        iterations,
        salt_b64,
        digest_b64 = encoded.split("$")

        salt = base64.urlsafe_b64decode(
            salt_b64.encode()
        )

        expected = base64.urlsafe_b64decode(
            digest_b64.encode()
        )

        actual = hashlib.pbkdf2_hmac(
            algorithm,
            password.encode(),
            salt,
            int(iterations)
        )

        return hmac.compare_digest(
            actual,
            expected
        )

    except (
        ValueError,
        TypeError
    ):
        return False