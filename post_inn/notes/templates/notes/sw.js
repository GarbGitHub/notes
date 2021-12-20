self.addEventListener('install',  async event => {
     console.log('[SW]: install')
});

self.addEventListener('activate', async event => {
  console.log('[SW]: activate')
});