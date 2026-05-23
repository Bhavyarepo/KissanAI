async function test() {
  try {
    // 1. Login
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

    // 2. Hit recommendations (proxied to Python)
    console.log("Hitting recommendations...");
    const recRes = await fetch('http://localhost:5000/api/recommendations/crops', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({
            location: "Pune",
            state: "Maharashtra",
            district: "Pune",
            season: "kharif"
        })
    });
    const text = await recRes.text();
    console.log("Success:", text);
  } catch (err) {
    console.error("Error:", err);
  }
}

test();
