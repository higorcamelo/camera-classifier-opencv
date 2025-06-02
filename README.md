# Camera Classifier

Um aplicativo simples que usa visão computacional para classificar objetos capturados pela câmera em tempo real.

## 🚀 Funcionalidades
- Coleta de imagens rápida e automática.
- Treinamento de modelo de classificação usando SVM.
- Predição em tempo real diretamente da câmera.
- Detecta quando nenhum dos objetos está presente ("Desconhecido") com base na confiança da predição.

## 🏗️ Tecnologias
- Python
- OpenCV
- Tkinter
- scikit-learn

## 🚀 Como usar
1. Execute:
   ```bash
   python main.py
   ```
2. Insira o nome de dois objetos.

3. Use os botões para capturar imagens de cada classe. O sistema irá parar automaticamente ao atingir 70 imagens.

4. Treine o modelo.

5. Clique em "Predizer" e veja o resultado na tela. Se nenhum dos objetos estiver presente, o sistema irá exibir "Desconhecido".

## Descrição dos Arquivos

- **camera.py**: Contém a classe `Camera` para capturar frames da webcam e converter de BGR para RGB.
- **model.py**: 
  - Classe `Model` que implementa uma SVM (`LinearSVC(max_iter=10000)`).
  - Métodos para treinar (`train_model`) e predizer (`predict`).
  - Pré-processamento de imagens em escala de cinza e resize para `150x150`.
- **app.py**: 
  - Classe `App` que monta a interface Tkinter.
  - Coleta automática de imagens, barras de progresso e contadores para as 3 classes.
  - Botões para treinar, predizer e resetar.
- **main.py**: Simples, executa `app.App()`.

## Possíveis Melhorias Futuras

- Trocar `LinearSVC` por `SVC(kernel='linear', probability=True)` para retornar probabilidades de predição.
- Implementar cross-validation e métricas de acurácia, precisão e recall.
- Adicionar suporte a mais classes (dividir janela de captura em seções dinâmicas).
- Interface mais moderna (Tkinter customizado, PyQt, ou web UI).
- Exportar o modelo treinado (`joblib.dump`) e permitir importação posterior (`joblib.load`).
