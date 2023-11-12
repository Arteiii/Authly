<script>
	import '@src/app.css';

	let products = [
		{
			id: 1,
			name: 'Appple',
			email: 'mail@apple.com',
			image:
				'https://images.unsplash.com/photo-1613588718956-c2e80305bf61?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=634&q=80',
			category: 'Technology',
			price: '200.00$',
			status: 'available'
		},
		{
			id: 2,
			name: 'Realme',
			email: 'mail@realme.com',
			image:
				'https://images.unsplash.com/photo-1423784346385-c1d4dac9893a?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80',
			category: 'Technology',
			price: '200.00$',
			status: 'no stock'
		},
		{
			id: 3,
			name: 'Samsung',
			email: 'mail@samsung.com',
			image:
				'https://images.unsplash.com/photo-1600856209923-34372e319a5d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2135&q=80',
			category: 'Technology',
			price: '200.00$',
			status: 'start sale'
		}
	];
</script>

<div class="col-span-40">
	<div class="overflow-auto lg:overflow-visible">
		<table class="table text-gray-400 border-separate space-y-6 text-sm">
			<thead class="bg-purple-600 text-white dark:bg-gray-800">
				<tr>
					<th class="p-3">Brand</th>
					<th class="p-3 text-left">Category</th>
					<th class="p-3 text-left">Price</th>
					<th class="p-3 text-left">Status</th>
					<th class="p-3 text-left">Action</th>
				</tr>
			</thead>
			<tbody>
				{#each products as product (product.id)}
					<tr class="bg-gray-100 dark:bg-gray-800">
						<td class="p-3">
							<div class="flex align-items-center">
								<img
									class="rounded-full  h-12 w-12 object-cover"
									src={product.image}
									alt={product.name}
								/>
								<div class="ml-3">
									<div class="text-gray-700 font-bold">{product.name}</div>
									<div class="text-gray-500">{product.email}</div>
								</div>
							</div>
						</td>
						<td class="p-3">{product.category}</td>
						<td class="p-3 font-bold">{product.price}</td>
						<td class="p-3">
							{#if product.status === 'available'}
								<span class="bg-green-400 text-gray-50 rounded-md px-2">{product.status}</span>
							{/if}
							{#if product.status === 'no stock'}
								<span class="bg-red-400 text-gray-50 rounded-md px-2">{product.status}</span>
							{/if}
							{#if product.status === 'start sale'}
								<span class="bg-yellow-400 text-gray-50 rounded-md px-2">{product.status}</span>
							{/if}
						</td>
						<td class="p-3">
							<a href="/" class="text-gray-400 hover:text-indigo-600 mr-2">
								<i class="material-icons-outlined text-base">visibility</i>
							</a>
							<a href="/" class="text-gray-400 hover:text-yellow-600 mx-2">
								<i class="material-icons-outlined text-base">edit</i>
							</a>
							<a href="/" class="text-gray-400 hover:text-red-600 ml-2">
								<i class="material-icons-round text-base">delete_outline</i>
							</a>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
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
