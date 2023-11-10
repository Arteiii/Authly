<script>
	import '@src/app.css';
    import BackButton from '@components/ui/buttons/BackButton.svelte';
</script>

<div>

    <BackButton />

	<main>
		<slot />
	</main>

	<footer>
	</footer>
</div>

