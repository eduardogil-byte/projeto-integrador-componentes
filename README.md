# 🔍 Sistema de Inspeção Automatizada de PCBs

Sistema de visão computacional desenvolvido para auxiliar na **inspeção de lotes de placas de circuito impresso (PCBs)**.

O projeto surgiu a partir de uma **demanda real apresentada por uma instituição da área de pesquisa**, que precisava verificar placas eletrônicas de forma mais rápida e padronizada.

A aplicação utiliza os arquivos de fabricação da placa juntamente com fotografias da PCB montada para localizar e verificar seus componentes.

> 🚧 Projeto em fase final de desenvolvimento e validação.

---

## 📌 Sobre o projeto

A inspeção manual de placas eletrônicas pode exigir a conferência de dezenas ou centenas de componentes em cada PCB.

Quando esse processo precisa ser repetido em vários exemplares de um mesmo lote, a inspeção pode se tornar demorada e sujeita a inconsistências.

O objetivo deste projeto é utilizar **visão computacional** para auxiliar esse processo.

O sistema recebe informações da fabricação da placa e uma imagem da PCB montada, realiza o alinhamento entre elas e verifica individualmente os componentes esperados.

---

## 🎯 Objetivo

O sistema foi desenvolvido para auxiliar na identificação de problemas como:

* componentes ausentes;
* componentes cuja presença não pôde ser confirmada;
* diferenças entre a placa montada e os dados esperados;
* problemas de alinhamento ou qualidade da imagem que impeçam uma inspeção confiável.

O objetivo não é apenas indicar um resultado, mas também facilitar a análise do operador durante a inspeção de um lote.

---

## 🧠 Como funciona

De forma simplificada, o processo de inspeção segue este fluxo:

```text
Arquivos da placa
        +
Foto da PCB montada
        ↓
Identificação da placa
        ↓
Alinhamento por homografia
        ↓
Localização dos componentes
        ↓
Recorte das regiões de interesse
        ↓
Análise por visão computacional
        ↓
Classificação dos componentes
        ↓
Resultado da inspeção
```

---

## 📐 Alinhamento da placa

Uma das etapas mais importantes do sistema é alinhar corretamente a fotografia da placa real com a referência utilizada pelo software.

Para isso, o sistema utiliza **homografia**, permitindo relacionar as coordenadas dos componentes presentes nos arquivos de fabricação com suas posições na fotografia.

Esse processo permite que o software saiba onde cada componente deveria estar mesmo quando a imagem apresenta diferenças de:

* posição;
* escala;
* perspectiva;
* rotação.

Caso o alinhamento não possua qualidade suficiente, o sistema evita realizar classificações que poderiam produzir resultados incorretos.

---

## 🔎 Inspeção dos componentes

Após o alinhamento, cada região correspondente a um componente é localizada e recortada.

Essas imagens são analisadas individualmente para determinar se o componente está presente.

Os resultados podem ser classificados em estados como:

```text
✅ Presente
⚠️ Incerto
❌ Ausente
```

Resultados considerados incertos podem ser posteriormente avaliados pelo operador.

---

## 🧩 Dados da placa

O sistema utiliza informações provenientes dos arquivos de fabricação da PCB para saber quais componentes devem estar presentes e onde eles estão posicionados.

Entre as informações utilizadas estão dados como:

* referência do componente;
* coordenadas X e Y;
* encapsulamento;
* posição esperada na placa.

Esses dados são combinados com a análise da imagem da placa montada.

---

## 🛠️ Tecnologias utilizadas

O projeto utiliza diferentes ferramentas de visão computacional e desenvolvimento de software, incluindo:

* **Python**
* **OpenCV**
* **YOLO**
* **MobileNet**
* **Processamento de imagens**
* **Homografia**
* **Gerber**
* **Dados de posicionamento de componentes**
* **HTML**
* **CSS**
* **JavaScript**

---

## 🤖 Visão computacional

O sistema combina diferentes técnicas para realizar a inspeção.

### OpenCV

Utilizado em etapas de processamento e análise das imagens, incluindo transformações, recortes e alinhamento.

### Homografia

Responsável por relacionar a imagem capturada da placa com o sistema de coordenadas utilizado pelos arquivos da PCB.

### MobileNet

Utilizada na análise das regiões dos componentes para auxiliar na classificação da presença dos componentes.

### YOLO

Utilizado como parte do processo de detecção e alinhamento visual da placa.

---

## 🖥️ Interface

O software também possui uma interface para facilitar o processo de inspeção.

A interface permite acompanhar os resultados obtidos pelo sistema e identificar rapidamente componentes que precisam de atenção.

A proposta é manter o operador dentro do processo, permitindo que casos inconclusivos possam ser avaliados manualmente.

---

## 🏭 Aplicação prática

O projeto foi desenvolvido pensando em um cenário real de inspeção de **lotes de placas eletrônicas**.

Em vez de verificar manualmente cada posição da placa, o operador pode utilizar o software como apoio para identificar rapidamente regiões que apresentam possíveis problemas.

Isso permite concentrar a inspeção humana nos componentes que realmente precisam de análise.

---

## 📊 Resultados da inspeção

Durante uma inspeção, o sistema analisa individualmente os componentes esperados na placa e gera um resultado para cada posição.

Esses resultados podem então ser utilizados para visualizar:

* componentes confirmados;
* componentes que precisam de revisão;
* possíveis ausências;
* problemas relacionados à captura da imagem ou alinhamento.

---

## 🚧 Status do projeto

O software encontra-se em **fase final de desenvolvimento e validação**.

Esta versão representa a primeira implementação do sistema de inspeção e serviu como base para novas melhorias e experimentos realizados durante a evolução do projeto.

---

## 🎓 Contexto

O projeto foi desenvolvido como **Projeto Integrador**, partindo de uma necessidade apresentada por uma instituição atuante na área de pesquisa.

A proposta permitiu aplicar conhecimentos de desenvolvimento de software e visão computacional em um problema real relacionado à inspeção de placas eletrônicas.

---

## 🧠 Conceitos aplicados

Durante o desenvolvimento foram aplicados conceitos como:

* visão computacional;
* processamento de imagens;
* homografia;
* detecção de objetos;
* classificação de imagens;
* transformação de coordenadas;
* processamento de arquivos de fabricação de PCBs;
* integração entre frontend e processamento de imagens;
* validação de resultados;
* desenvolvimento orientado a uma necessidade real.

---

## 👨‍💻 Autores

**Eduardo Machado Gil**
GitHub: [@eduardogil-byte](https://github.com/eduardogil-byte)

**Luiz Gustavo da Silva Campos**
GitHub: [@luizcamposss](https://github.com/luizcamposss)
