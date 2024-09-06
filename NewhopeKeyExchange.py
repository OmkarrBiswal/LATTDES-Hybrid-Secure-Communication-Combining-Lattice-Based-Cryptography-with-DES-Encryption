import numpy as np

# Parameters
n = 256  # Dimension of the ring
q = 12289  # Modulus
sigma = 8.0  # Standard deviation for error distribution
m = 1024  # Number of samples for error distribution

def generate_secret_key():
    return np.random.randint(q, size=n)

def generate_public_key(secret_key):
    a = np.random.randint(q, size=n)
    e = np.random.normal(scale=sigma, size=n)
    b = np.polyadd(np.polymul(a, secret_key), np.round(e).astype(int)) % q
    return (a, b)

def compute_shared_secret(secret_key, received_public_key):
    a_received, b_received = received_public_key
    s_b = np.polymul(secret_key, a_received) % q
    e = np.array(b_received) - (s_b + q//2) % q
    return np.round(e).astype(int)

# Alice's side
alice_secret_key = generate_secret_key()
alice_public_key = generate_public_key(alice_secret_key)

# Bob's side
bob_secret_key = generate_secret_key()
bob_public_key = generate_public_key(bob_secret_key)

# Alice sends her public key to Bob
# Bob receives Alice's public key
# Bob computes shared secret using his secret key and Alice's public key
bob_shared_secret = compute_shared_secret(bob_secret_key, alice_public_key)

# Bob sends his public key to Alice
# Alice receives Bob's public key
# Alice computes shared secret using her secret key and Bob's public key
alice_shared_secret = compute_shared_secret(alice_secret_key, bob_public_key)

# Ensure both shared secrets match
print("Shared secrets match:", np.array_equal(bob_shared_secret, alice_shared_secret))
