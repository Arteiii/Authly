<script>
  import { createEventDispatcher } from 'svelte';

  let isLoading = false;
  const dispatch = createEventDispatcher();

  function handleClick() {
    isLoading = true;

    // Simulate asynchronous task
    setTimeout(() => {
      isLoading = false;
      dispatch('complete');
    }, 2000); // Change the timeout duration as needed
  }
</script>

<button
  on:click={handleClick}
  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
  disabled={isLoading}
>
  {#if isLoading}
    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647zM12 20c-4.418 0-8-3.582-8-8h-4c0 6.627 5.373 12 12 12v-4zm2-5.291A7.962 7.962 0 0120 12h4c0-3.042-1.135-5.824-3-7.938l-3 2.647z"></path>
    </svg>
    Loading
  {:else}
    Toggle Button
  {/if}
</button>

