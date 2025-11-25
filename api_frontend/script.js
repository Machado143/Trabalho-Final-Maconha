const { createApp } = Vue;

createApp({
    data() {
        return {
            plantas: [],
            loading: true,
            error: null
        }
    },
    mounted() {
        this.carregarPlantas();
    },
    methods: {
        async carregarPlantas() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/plantas/');
                this.plantas = response.data.results || response.data;
                this.loading = false;
            } catch (error) {
                console.error('Erro ao carregar plantas:', error);
                this.error = 'Erro ao conectar com a API';
                this.loading = false;
            }
        }
    }
}).mount('#app');   