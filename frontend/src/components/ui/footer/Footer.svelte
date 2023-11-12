<script>
	// You can add more contributors as needed
	const contributors = ['wavy42', 'arteii'];
	const repoUrl = 'https://github.com/wavy42/Authly';

	// Function to open the GitHub repository in a new tab
	function openRepo() {
		window.open(repoUrl, '_blank');
	}
	// Function to handle keyboard events (enter key)
	function handleKeyPress(event) {
		if (event.key === 'Enter') {
			openRepo();
		}
	}
</script>

<div class="container mx-auto text-center">
	<p class="mb-2">Made with ❤️ by:</p>
	<div class="flex items-center justify-center space-x-2">
		{#each contributors as contributor}
			<span>{contributor}</span>
		{/each}
	</div>
	<p class="mt-2">and other contributors</p>
	<p class="mt-2">
		Project source code available on
		<span
			role="button"
			tabindex="0"
			class="cursor-pointer text-blue-500"
			on:click={openRepo}
			on:keypress={handleKeyPress}>GitHub</span
		>.
	</p>
</div>
