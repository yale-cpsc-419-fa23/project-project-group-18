<template>
  <main>
    <div id="top-left-icon">
      <IconComponent :icon-src="icon" />
    </div>
    <router-view></router-view>
  </main>
</template>

<script setup>
import { ref, watchEffect, computed } from 'vue';
import LightIcon from '@/assets/instaGame-light.svg';
import DarkIcon from '@/assets/instaGame-dark.svg';
import IconComponent from './components/IconComponent.vue';

const theme = ref(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

const icon = computed(() => {
  return theme.value === 'dark' ? DarkIcon : LightIcon;
});

// Listen for system theme changes
watchEffect(() => {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  mediaQuery.addEventListener('change', (e) => {
    theme.value = e.matches ? 'dark' : 'light';
  });
});
</script>

<style scoped>
#top-left-icon {
  position: absolute;
  top: 1%;
  left: 20%;
  max-width: 50px !important;
  max-height: 50px !important;
  /* width: 50px; 
  height: 50px;  */
}

#top-left-icon svg {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* This ensures the SVG scales within its container */
}
</style>
