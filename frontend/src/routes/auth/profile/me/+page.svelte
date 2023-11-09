<script>
  let fetchedData = null;
  let error = null;


  async function fetchData() {
    // Retrieve the authentication token from local storage
    const authToken = localStorage.getItem('authToken');

    if (!authToken) {
      error = 'Authentication token is missing. Please log in.';
      return;
    }

    try {
      const response = await fetch('http://192.168.178.58:8000/api/v1/user/users/me/', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      });

      if (response.ok) {
        fetchedData = await response.json();
        error = null;
      } else {
        error = 'Failed to fetch data. Please try again.';
        fetchedData = null;
      }
    } catch (err) {
      console.error('Error:', err);
      error = 'An error occurred while fetching data.';
      fetchedData = null;
    }
  }
</script>

<h1>Authenticated Page</h1>

<button on:click={fetchData}>Fetch Data</button>

{#if error}
  <p>{error}</p>
{/if}

{#if fetchedData}
  <h2>Fetched Data</h2>
  <pre>{JSON.stringify(fetchedData, null, 2)}</pre>
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

  section {
    background-color: var(--background-color);
    color: var(--text-color);
  }
</style>