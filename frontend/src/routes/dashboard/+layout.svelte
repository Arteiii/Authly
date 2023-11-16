<script>    
	import Sidebar from './Sidebar.svelte';
	import '@src/app.css';
	import Backdrop from './Backdrop.svelte';
	import Footer from '@ui/footer/Footer.svelte';

</script>

<div>


	<main>
		<div class="flex h-screen">
			<Sidebar></Sidebar>
			<Backdrop></Backdrop>
			
		</div>

		<slot />
	</main>

	<footer class="bg-slate-950 text-gray-300 p-4">
		<Footer />
	</footer>
</div>

