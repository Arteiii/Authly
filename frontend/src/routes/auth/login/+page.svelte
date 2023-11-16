<script>
  import { navigate } from 'svelte-routing';
  import Button from '@components/ui/buttons/Button.svelte';

  let isLoading = false;
  let isError = false;
  let isDone = false;

  let username = "";
  let password = "";
  let loginStatus = "";




  async function loginUser() {
    isLoading = true;
    const grantType = "password";
    const clientSecret = "your_client_secret"; // Replace with your client secret
    const scope = "your_scope"; // Replace with the required scope

    // Encode the password to base64 on the client side
    const passwordBase64 = btoa(password);

    const formData = new FormData();
    formData.append("grant_type", grantType);
    formData.append("username", username);
    formData.append("password", passwordBase64);
    formData.append("scope", scope);

    try {
      const response = await fetch('http://192.168.178.58:8000/api/v1/user/token/', {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${btoa(clientSecret)}`, // Base64 encode the client secret
        },
        body: formData,
      });

      if (response.ok) {
        isLoading = false;
        
        const data = await response.json();
        const accessToken = data.access_token;
        
        // Save the access token in localStorage
        localStorage.setItem('authToken', accessToken);
        
        isDone = true;

        loginStatus = 'Login successful!';
        handleComplete()
      } else {
          const errorData = await response.json();
          PopupMessage.showMessage(errorData.detail);
          handleButtonError()
      }
    } catch (error) {
      handleButtonError()
      const errorData = await response.json();
      PopupMessage.showMessage(errorData.detail);
    }
  }
  function handleComplete() {
    // Introduce a delay of 2 seconds before navigating to the new page
    setTimeout(() => {
      navigate('/dashboard');
    }, 2000);
  }
  function handleButtonError(time=5000) {
    isLoading = false;
    isDone = false;
    isError = true;
    setTimeout(() => {
      isLoading = false;
      isDone = false;
      isError = false;
    }, time);
  }
</script>

<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-sm">
    <!-- <img class="mx-auto h-10 w-auto" src="" alt="Authly"> -->
    <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900 dark:text-gray-200">Sign in to your account</h2>
  </div>

  <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
    <form class="space-y-6" action="#" method="POST">
      <div>
        <label for="email" class="block text-sm font-medium leading-6 text-gray-900 dark:text-gray-200 ">Email address</label>
        <div class="mt-2">
          <input id="email" bind:value={username}  name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
        </div>
      </div>

      <div>
        <div class="flex items-center justify-between">
          <label for="password" class="block text-sm font-medium leading-6 text-gray-900 dark:text-gray-200">Password</label>
          <div class="text-sm">
            <a href="/404" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
          </div>
        </div>
        <div class="mt-2">
          <input bind:value={password} id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
        </div>
      </div>

      <div class="flex min-h-full items-center justify-center px-6 lg:px-8">
        <Button 
          on:click={loginUser}
          loading={isLoading} 
          loadingClass="bg-yellow-600 scale-110 active:bg-yellow-600" 
          error={isError} 
          errorClass="bg-red-600 scale-110 shake active:bg-red-600"
          done={isDone} 
          doneClass="bg-green-600 scale-110 active:bg-green-600"
        >
          {#if isLoading}
            Loading...
          {:else if isError}
              Error! try again
          {:else if isDone}
              Successfully
          {:else}
              Login!
          {/if}
        </Button>
      </div>
    </form>
    <p class="mt-10 text-center text-sm text-gray-500">
      Not a member?
      <a href="/auth/register" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Register</a>
    </p>
  </div>
</div>


<style lang="postcss">
</style>