<script>
  let username = "";
  let password = "";
  let loginStatus = "";

  async function loginUser() {
    const grantType = "password";
    const clientSecret = "your_client_secret"; // Replace with your client secret
    const scope = "your_scope"; // Replace with the required scope

    // Encode the password to base64 on the client side
    const passwordBase64 = btoa(password);

    const formData = new FormData();
    formData.append("grant_type", grantType);
    formData.append("username", username);
    formData.append("password", passwordBase64); // Send the base64-encoded password
    formData.append("scope", scope);

    try {
      const response = await fetch('http://localhost:8000/api/v1/user/token/', {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${btoa(clientSecret)}`, // Base64 encode the client secret
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        const accessToken = data.access_token;

        // Save the access token in localStorage
        localStorage.setItem('authToken', accessToken);

        loginStatus = 'Login successful! Access Token: ...'; // Include the access token here
      } else {
        loginStatus = 'Login failed. Please check your credentials and try again.';
      }
    } catch (error) {
      console.error('Error:', error);
      loginStatus = 'An error occurred while logging in.';
    }
  }
</script>

<h1>Login</h1>

<label for="username">Email:</label>
<input type="text" id="username" bind:value={username} />

<label for="password">Password:</label>
<input type="password" id="password" bind:value={password} />

<button on:click={loginUser}>Login</button>

{#if loginStatus}
  <p>{loginStatus}</p>
{/if}