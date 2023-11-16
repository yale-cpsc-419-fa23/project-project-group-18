<template>
	
	<div>
		Game: {{ gameType }}
	</div> 

</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { useRoute } from 'vue-router';

	const route = useRoute();
	const gameType = ref('');

	onMounted(() => {
		console.log("enter room")
		gameType.value = route.query.gameType;
	});

</script>