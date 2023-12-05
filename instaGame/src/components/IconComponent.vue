<template>
    <img :src="iconSrc" alt="Icon" class="icon-image" />
</template>
  
<script setup>
import { defineProps } from 'vue';

const props = defineProps({
iconSrc: String
});
</script>

<style scoped>
.icon-image {
  width: 100%;
  height: 100%;
}
</style>