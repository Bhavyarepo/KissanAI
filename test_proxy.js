async function test() {
  try {
    // 1. Register a test user
    try {
        await fetch('http://localhost:5000/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: "Test User",
                email: "test5@example.com",
                phone: "1234567895",
                location: "Test",
                state: "Test",
                district: "Test",
                password: "password123"
            })
        });
    } catch (e) {
        // Ignore if exists
    }

    // 2. Login
    const loginRes = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: "test5@example.com",
            password: "password123"
        })
    });
    const loginData = await loginRes.json();
    const token = loginData.access_token;
    console.log("Got token:", token);

    // 3. Hit recommendations (proxied to Python)
    console.log("Hitting recommendations...");
    const recRes = await fetch('http://localhost:5000/api/recommendations/history', {
        headers: { Authorization: `Bearer ${token}` }
    });
    const text = await recRes.text();
    console.log("Success:", text);
  } catch (err) {
    console.error("Error:", err);
  }
}

test();
