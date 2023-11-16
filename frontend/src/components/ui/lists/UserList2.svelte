<script>
	import '@src/app.css';

	let currentPage = 0;
	const usersPerPageOptions = [5, 10, 20]; // Add other options as needed
	let usersPerPage = 12; // Default value

	export let users = [];

	function changePage(page) {
		console.log(page);
		currentPage = page;
		console.log('curretn page:', page);
	}

	$: start = currentPage * usersPerPage;
	$: end = start + usersPerPage;
	$: displayedUsers = users.slice(start, end);
	$: totalUsers = users.length;
	$: totalPages = Math.ceil(totalUsers / usersPerPage);
	$: showPagination = totalPages > 1;
</script>

<div class="w-full overflow-x-auto">
	<table class="max-h-screen overflow-y-auto w-full">
		<div class="w-full">
			<div class="overflow-auto lg:overflow-visible mx-auto">
				<table
					class="table text-gray-400 border-separate space-y-6 text-sm overflow-auto w-full whitespace-no-wrap"
				>
					<thead class="bg-purple-600 text-white dark:bg-gray-800">
						<tr>
							<th class="p-3 text-left">Brand</th>
							<th class="p-3 text-left">Category</th>
							<th class="p-3 text-left">Price</th>
							<th class="p-3 text-left">Status</th>
							<th class="p-3 text-left">Action</th>
						</tr>
					</thead>
					<tbody>
						{#each displayedUsers as user (user.id)}
							<tr class="bg-gray-100 dark:bg-gray-800">
								<td class="p-3">
									<div class="flex align-items-center">
										<img
											class="rounded-full h-12 w-12 object-cover"
											src={user.image}
											alt={user.name}
										/>
										<div class="ml-3">
											<div class="text-gray-700 font-bold">{user.name}</div>
											<div class="text-gray-500">{user.email}</div>
										</div>
									</div>
								</td>
								<td class="p-3">{user.category}</td>
								<td class="p-3 font-bold">{user.price}</td>
								<td class="p-3">
									{#if user.status === 'available'}
										<span class="bg-green-400 text-gray-50 rounded-md px-2">{user.status}</span>
									{/if}
									{#if user.status === 'no stock'}
										<span class="bg-red-400 text-gray-50 rounded-md px-2">{user.status}</span>
									{/if}
									{#if user.status === 'start sale'}
										<span class="bg-yellow-400 text-gray-50 rounded-md px-2">{user.status}</span>
									{/if}
								</td>
								<td class="p-3">
									<a href="/" class="text-gray-400 hover:text-indigo-600 mr-2">
										<i class="material-icons-outlined text-base text-right">visibility</i>
									</a>
									<a href="/" class="text-gray-400 hover:text-yellow-600 mx-2">
										<i class="material-icons-outlined text-base text-center">edit</i>
									</a>
									<a href="/" class="text-gray-400 hover:text-red-600 ml-2">
										<i class="material-icons-round text-base text-right">delete_outline</i>
									</a>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</table>
</div>
<div
	class="grid px-4 py-3 mb-10 text-xs font-semibold tracking-wide text-gray-500 uppercase border-t dark:border-gray-700 bg-purple-600 sm:grid-cols-9 dark:text-white dark:bg-gray-800 rounded-lg"
>
	{#if showPagination}
		<span class="flex items-center col-span-3 text-white">
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
								class="px-3 py-1 rounded-md rounded-l-lg focus:outline-none focus:shadow-outline-purple bg-white text-purple-600 dark:bg-transparent dark:text-white"
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
									? 'px-3 py-1 text-white transition-colors duration-150 bg-purple-600 border border-r-0 border-purple-600 rounded-md focus:outline-none focus:shadow-outline-purple  dark:border-purple-600'
									: 'px-3 py-1 rounded-md focus:outline-none focus:shadow-outline-purple bg-white text-purple-600 dark:bg-transparent dark:text-white'}
							>
								{page + 1}
							</button>
						</li>
					{/each}

					{#if currentPage < totalPages - 1}
						<li>
							<button
								on:click={() => changePage(currentPage + 1)}
								class="px-3 py-1 rounded-md rounded-r-lg focus:outline-none focus:shadow-outline-purple bg-white text-purple-600 dark:bg-transparent dark:text-white"
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

<style>
	.table {
		border-spacing: 0 15px;
	}

	i {
		font-size: 1rem !important;
	}

	.table tr {
		border-radius: 20px;
	}

	tr td:nth-child(n + 5),
	tr th:nth-child(n + 5) {
		border-radius: 0 0.625rem 0.625rem 0;
	}

	tr td:nth-child(1),
	tr th:nth-child(1) {
		border-radius: 0.625rem 0 0 0.625rem;
	}
</style>
