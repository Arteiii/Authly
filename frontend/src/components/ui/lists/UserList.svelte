<script>
  import '@src/app.css'
  export let users = [
    {
      name: 'John Doe',
      email: 'john.doe@example.com',
      image: 'https://placekitten.com/100/100',
      role: 'Admin',
      status: true,
      lastSeen: new Date().toISOString(),
    },
    {
      name: 'Jane Smith',
      email: 'jane.smith@example.com',
      image: 'https://placekitten.com/101/101',
      role: 'User',
      status: false,
      lastSeen: new Date(new Date().getTime() - 2 * 60 * 60 * 1000).toISOString(),
    },
    // Add more users as needed
  ];
</script>

<ul role="list" class="divide-y divide-gray-100">
  {#each users as user}
    <li class="flex justify-between gap-x-6 py-5">
      <div class="flex min-w-0 gap-x-4">
        <img class="h-12 w-12 flex-none rounded-full bg-gray-50" src={user.image} alt="">
        <div class="min-w-0 flex-auto">
          <p class="text-sm font-semibold leading-6 text-gray-900">{user.name}</p>
          <p class="mt-1 truncate text-xs leading-5 text-gray-500">{user.email}</p>
        </div>
      </div>
      <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
        {#if user.role}
          <p class="text-sm leading-6 text-gray-900">{user.role}</p>
        {/if}
        {#if user.status}
          <div class="mt-1 flex items-center gap-x-1.5">
            <div class="flex-none rounded-full bg-emerald-500/20 p-1">
              <div class="h-1.5 w-1.5 rounded-full bg-emerald-500"></div>
            </div>
            <p class="text-xs leading-5 text-gray-500">Online</p>
          </div>
        {/if}
        {#if user.lastSeen}
          <p class="mt-1 text-xs leading-5 text-gray-500">Last seen <time datetime={user.lastSeen}>3h ago</time></p>
        {/if}
      </div>
    </li>
  {/each}
</ul>