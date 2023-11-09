<script>
  let username = "";
  let email = "";
  let password = "";
  let registrationStatus = "";


  async function registerUser() {
    // Encode the password to base64
    const passwordBase64 = btoa(password);
    const userData = { username, email, password: passwordBase64 };

    try {
      const response = await fetch('http://192.168.178.58:8000/api/v1/user/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        registrationStatus = 'User registered successfully!';
      } else {
        registrationStatus = 'User registration failed. Please try again.';
      }
    } catch (error) {
      console.error('Error:', error);
      registrationStatus = 'An error occurred while registering the user.';
    }
  }
</script>

<h1>Register User</h1>

<label for="username">Username:</label>
<input type="text" id="username" bind:value={username} />

<label for="email">Email:</label>
<input type="email" id="email" bind:value={email} />

<label for="password">Password:</label>
<input type="password" id="password" bind:value={password} />

<button class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow" on:click={registerUser}>Register</button>

{#if registrationStatus}
  <p>{registrationStatus}</p>
{/if}


<style lang="postcss">
  :global(html) {
    --background-color: white;
    --text-color: black;
  }

  @media (prefers-color-scheme: dark) {
    :global(html) {
      --background-color: black;
      --text-color: white;
    }
  }
</style>