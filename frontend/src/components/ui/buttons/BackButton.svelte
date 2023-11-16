<script>
	import { onMount } from 'svelte';
	export let destination = '/';
</script>

<div class="mt-4 flex items-center cursor-pointer" role="button" tabindex="0" aria-label="Go back">
	<a href={destination}>
		<button
			type="button"
			class="w-full flex items-center justify-center px-5 py-2 text-sm font-semibold leading-6 text-gray-900 transition-colors duration-200 gap-x-2 sm:w-auto dark:text-gray-200"
		>
			<span>&larr; Go back</span>
		</button>
	</a>
</div>

<style>
	/* Add any necessary styling here */
	.flex {
		display: flex;
	}

	.items-center {
		align-items: center;
	}

	.cursor-pointer {
		cursor: pointer;
	}

	/* Customize the styling as needed */
</style>
