async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('status');

    if (!fileInput.files.length) {
        status.textContent = 'Selecione um arquivo primeiro!';
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    status.textContent = "Enviando arquivo...";

    try {
        console.log("📤 Enviando arquivo:", file.name);

        const response = await fetch('https://gk52y82w0h.execute-api.us-east-1.amazonaws.com/Prod/api/v1/invoice', {
            method: 'POST',
            body: formData,
            headers: {
                "Accept": "application/json"
            }
        });

        console.log("🔄 Resposta da API:", response);

        const result = await response.json();

        if (response.ok) {
            status.textContent = "✅ Arquivo enviado com sucesso!";
        } else {
            status.textContent = "❌ Erro: " + (result.message || "Falha ao enviar arquivo.");
        }

        console.log("📜 Detalhes da resposta:", result);
    } catch (error) {
        status.textContent = '⚠️ Erro ao enviar o arquivo';
        console.error("🚨 Erro ao fazer a requisição:", error);
    }
}
