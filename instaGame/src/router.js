import { createRouter, createWebHistory } from 'vue-router';
import Lobby from './views/Lobby.vue';
import Game from './views/Game.vue';

const routes = [
  { path: '/', component: Lobby },
  { path: '/game', component: Game },
  // ... other routes
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
