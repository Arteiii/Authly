<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let currentPage;
  export let totalUsers;
  export let usersPerPage = 8; // Default value

  function changePage(page) {
    dispatch('change', { page, usersPerPage });
  }

  function handleUsersPerPageChange(event) {
    usersPerPage = +event.target.value; // Convert to a number
    changePage(0); // Reset to the first page when changing users per page
  }

  $: totalPages = Math.ceil(totalUsers / usersPerPage);
  $: showPagination = totalPages > 1; // Check if pagination controls should be displayed
</script>

<div
  class="grid px-4 py-3 text-xs font-semibold tracking-wide text-gray-500 uppercase border-t dark:border-gray-700 bg-gray-50 sm:grid-cols-9 dark:text-gray-400 dark:bg-gray-800"
>
  {#if showPagination}
    <span class="flex items-center col-span-3">
      Showing {currentPage * usersPerPage + 1}-{Math.min(
        (currentPage + 1) * usersPerPage,
        totalUsers
      )} of {totalUsers}
    </span>
    <span class="col-span-2" />

    <span class="flex col-span-4 mt-2 sm:mt-auto sm:justify-end">
      <nav aria-label="Table navigation">
        <ul class="inline-flex items-center">
          {#if currentPage > 0}
            <li>
              <button
                on:click={() => changePage(currentPage - 1)}
                class="px-3 py-1 rounded-md rounded-l-lg focus:outline-none focus:shadow-outline-purple"
                aria-label="Previous"
              >
                <svg aria-hidden="true" class="w-4 h-4 fill-current" viewBox="0 0 20 20">
                  <path
                    d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                    fill-rule="evenodd"
                  />
                </svg>
              </button>
            </li>
          {/if}

          {#each Array.from({ length: totalPages }, (_, i) => i) as page}
            <li>
              <button
                on:click={() => changePage(page)}
                class={page === currentPage
                  ? 'px-3 py-1 text-white transition-colors duration-150 bg-purple-600 border border-r-0 border-purple-600 rounded-md focus:outline-none focus:shadow-outline-purple'
                  : 'px-3 py-1 rounded-md focus:outline-none focus:shadow-outline-purple'}
              >
                {page + 1}
              </button>
            </li>
          {/each}

          {#if currentPage < totalPages - 1}
            <li>
              <button
                on:click={() => changePage(currentPage + 1)}
                class="px-3 py-1 rounded-md rounded-r-lg focus:outline-none focus:shadow-outline-purple"
                aria-label="Next"
              >
                <svg class="w-4 h-4 fill-current" aria-hidden="true" viewBox="0 0 20 20">
                  <path
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                    fill-rule="evenodd"
                  />
                </svg>
              </button>
            </li>
          {/if}
        </ul>
      </nav>
    </span>
  {/if}
</div>
