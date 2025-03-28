document.getElementById("fileInput").addEventListener("change", function(event) {
    const file = event.target.files[0];
    const fileNameElement = document.getElementById("fileName");

    if (file) {
        fileNameElement.textContent = `📄 Arquivo selecionado: ${file.name}`;
    } else {
        fileNameElement.textContent = "";
    }
});

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('status');
    const fileNameElement = document.getElementById("fileName");

    if (!fileInput.files.length) {
        status.textContent = '⚠️ Selecione um arquivo primeiro!';
        status.style.color = 'red';
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    status.textContent = "📤 Enviando arquivo...";
    status.style.color = "#007bff"; 

    try {
        console.log("📤 Enviando arquivo:", file.name);

        const response = await fetch('https://ejbp0hc13c.execute-api.us-east-1.amazonaws.com/Prod/api/v1/invoice', {
            method: 'POST',
            body: formData,
            headers: { "Accept": "application/json" }
        });

        console.log("🔄 Resposta da API:", response);

        let result;
        try {
            result = await response.json();
        } catch (jsonError) {
            console.error("❌ Erro ao processar JSON:", jsonError);
            throw new Error("A resposta da API não está no formato esperado.");
        }

        if (response.ok) {
            status.textContent = "✅ Arquivo enviado com sucesso!";
            status.style.color = "green";
            fileNameElement.textContent = ""; // Limpa o nome do arquivo após envio
            fileInput.value = ""; // Reseta o input de arquivo
        } else {
            throw new Error(result.message || "Erro desconhecido ao enviar o arquivo.");
        }

        console.log("📜 Detalhes da resposta:", result);
    } catch (error) {
        status.textContent = `❌ ${error.message}`;
        status.style.color = "red";
        console.error("🚨 Erro ao fazer a requisição:", error);
    }
}
