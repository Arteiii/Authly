<script>    
	import Sidebar from './Sidebar.svelte';
	import '@src/app.css';
	import Backdrop from './Backdrop.svelte';
</script>

<div>


	<main>
		<div class="flex h-screen">
			<Sidebar></Sidebar>
			<Backdrop></Backdrop>
			
		</div>

		<slot />
	</main>

	<footer>
	</footer>
</div>

