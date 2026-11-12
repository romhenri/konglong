# Dinossauros e Clados: base de conhecimento RDF/OWL

base de conhecimento modelada com RDF, RDFS e OWL em Turtle (`dinossauros.ttl`) e consultada com rdflib e SPARQL (`consultas.py`).

**Sumário:** [Placar dos requisitos](#placar-dos-requisitos) · [Resumo da base](#resumo-da-base) · [Taxonomia](#taxonomia-hierarquia-de-classes) · [Propriedades](#propriedades) · [Construções OWL](#construções-owl-e-justificativa) · [Consultas](#consultas) · [O rdflib não raciocina](#o-rdflib-não-raciocina-como-as-consultas-compensam) · [Como executar](#como-executar)

## Placar dos requisitos

| Requisito do roteiro | Mínimo | Entregue | Onde comprovar |
|---|---|---|---|
| Hierarquia `rdfs:subClassOf` | 8 classes, 2 níveis abaixo da raiz | 33 classes; 4 níveis abaixo de Dinossauro (Saurischia › Theropoda › Coelurosauria › Tyrannosauridae) | `dinossauros.ttl` 24–158 · consulta 1.4 |
| Propriedades com domain/range | 10 (5 de objeto + 5 de dados) | 10 de objeto + 7 de dados, todas com domain e range | `dinossauros.ttl` 198–308 |
| Instâncias com valores plausíveis | 25 | 167 (63 espécies, 11 intervalos, 36 formações, 14 países, 43 paleontólogos) | consulta `[0]` · [Fontes dos dados](#fontes-dos-dados) |
| Triplas | 50 | 1169 | consulta `[0]` |
| Construções OWL justificadas | 5 | 8 tipos distintos | [Construções OWL](#construções-owl-e-justificativa) · consulta 1.6 |
| Consultas `g.triples()` variando padrões | 5 | 7, cobrindo todas as combinações de fixo/`None` | [Parte 1](#parte-1-gtriples) |
| SELECT com FILTER e com ORDER BY/agregação | 1 de cada | 5 SELECTs (2.1 FILTER + ORDER BY; 2.2 e 2.5 agregação) | 2.1–2.5 |
| ASK | 1 | 2 (um `false`, um `true`) | 2.6, 2.7 |
| CONSTRUCT | 1 | 1, gera 51 triplas inferidas | 2.8 |
| Update: INSERT, DELETE, DELETE/INSERT | 1 de cada | 3, com antes/depois impresso | 2.9, 2.10, 2.11 |
| App Python que carrega o `.ttl` e imprime cada consulta com número e propósito | sim | `Graph().parse(...)` e cabeçalho `[n] propósito` em cada consulta | `consultas.py` |
| README com resumo, entidades, taxonomia e como executar | sim | este arquivo | [Como executar](#como-executar) |

## Resumo da base

A base descreve **63 espécies de dinossauros** reais, do Triássico Médio ao fim do Cretáceo, classificadas por **clados** (Saurischia, Theropoda, Ceratopsia...), situadas na **escala de tempo geológico** (Era > Período > Época), ligadas às **formações geológicas** e aos **países** onde foram encontradas, e aos **paleontólogos** que as descreveram. Também registra relações de **predação** com evidência fóssil (ex.: os "Dinossauros Lutadores", Velociraptor x Protoceratops). Inclui oito espécies brasileiras: Irritator, Mirischia, Saturnalia, Staurikosaurus, Gnathovorax, Buriolestes, Unaysaurus e Austroposeidon.

| Item | Quantidade | Mínimo |
|---|---|---|
| Triplas | 1169 | 50 |
| Classes | 33 | 8 |
| Propriedades de objeto | 10 | 5 |
| Propriedades de dados | 7 | 5 |
| Indivíduos | 167 | 25 |
| Tipos de construção OWL | 8 | 5 |

Esses números são recalculados e impressos pela própria aplicação (consulta `[0]`). O `.ttl` é carregado com `Graph().parse(TTL, format="turtle")` na primeira linha do programa; se houvesse erro de sintaxe, nada mais rodaria.

<details>
<summary>Saída real da consulta [0]</summary>

```
[0] Estatisticas da base x minimos do roteiro
------------------------------------------------------------------------
  Triplas                    1169  (minimo 50) OK
  Classes                      33  (minimo 8) OK
  Propriedades de objeto       10  (minimo 5) OK
  Propriedades de dados         7  (minimo 5) OK
  Individuos                  167  (minimo 25) OK
  Tipos de construcao OWL       8  (minimo 5) OK
  Construcoes OWL usadas:
    - owl:TransitiveProperty: 1
    - owl:FunctionalProperty: 5
    - owl:AsymmetricProperty: 1
    - owl:inverseOf: 3
    - owl:propertyChainAxiom: 1
    - owl:disjointWith: 1
    - owl:AllDisjointClasses: 1
    - owl:equivalentClass + owl:Restriction: 1
```

</details>

## Taxonomia (hierarquia de classes)

A taxonomia de dinossauros é naturalmente profunda: chega a **4 níveis abaixo da raiz** `Dinossauro`.

```
Dinossauro                      Nyasasaurus (posição incerta)
├── Saurischia            (quadril de lagarto)   Herrerasaurus, Staurikosaurus (BR), Gnathovorax (BR)
│   ├── Theropoda         (bípedes, maioria carnívora)   Coelophysis, Dilophosaurus, Megalosaurus
│   │   ├── Ceratosauria            Ceratosaurus
│   │   │   └── Abelisauridae       Carnotaurus, Majungasaurus
│   │   ├── Coelurosauria           Yutyrannus, Sinosauropteryx, Oviraptor, Mirischia (BR)
│   │   │   ├── Tyrannosauridae     Tyrannosaurus rex, Albertosaurus, Tarbosaurus
│   │   │   ├── Dromaeosauridae     Velociraptor, Deinonychus, Microraptor, Utahraptor
│   │   │   └── Ornithomimosauria   Gallimimus, Struthiomimus
│   │   ├── Spinosauridae           Spinosaurus, Irritator (BR)
│   │   └── Allosauroidea           Allosaurus
│   │       └── Carcharodontosauridae   Giganotosaurus, Carcharodontosaurus, Acrocanthosaurus, Mapusaurus
│   └── Sauropodomorpha             Saturnalia (BR), Buriolestes (BR), Unaysaurus (BR), Plateosaurus, Massospondylus
│       └── Sauropoda               Brachiosaurus, Camarasaurus, Mamenchisaurus, Shunosaurus
│           ├── Diplodocidae        Diplodocus, Apatosaurus, Brontosaurus
│           └── Titanosauria        Argentinosaurus, Patagotitan, Rapetosaurus, Austroposeidon (BR)
├── Ornithischia          (quadril de ave)   Heterodontosaurus
│   ├── Ornithopoda                 Iguanodon, Tenontosaurus
│   │   └── Hadrosauridae           Edmontosaurus, Parasaurolophus, Corythosaurus, Maiasaura
│   ├── Ceratopsia                  Protoceratops, Psittacosaurus
│   │   └── Ceratopsidae            Triceratops, Styracosaurus
│   ├── Pachycephalosauria          Pachycephalosaurus
│   └── Thyreophora                 Scelidosaurus
│       ├── Stegosauria             Stegosaurus, Kentrosaurus
│       └── Ankylosauria            Ankylosaurus, Euoplocephalus
└── Predador              (classe definida por restrição OWL)

IntervaloGeologico
├── Era        Mesozoico
├── Periodo    Triassico, Jurassico, Cretaceo
└── Epoca      Triassico Medio/Superior, Jurassico Inferior/Medio/Superior, Cretaceo Inferior/Superior

FormacaoGeologica   Hell Creek, Morrison, Santa Maria, Romualdo, Dinosaur Park, Nemegt, ... (36)
Pais                Brasil, Argentina, EUA, Canada, China, Mongolia, ... (14)
Paleontologo        Marsh, Cope, Osborn, Owen, Coria, Langer, Xu Xing, ... (43)
```

**Decisão de modelagem: clado é classe, espécie é indivíduo do clado mais específico.** Assim, `Tyrannosaurus_rex a Tyrannosauridae` basta; a pertinência a Coelurosauria, Theropoda, Saurischia e Dinossauro decorre de `rdfs:subClassOf`, sem repetir tipos, e é recuperada nas consultas com o caminho SPARQL `rdf:type/rdfs:subClassOf*`. A espécie é indivíduo porque os fatos são dela (comprimento, massa, ano, autor) e ela recebe propriedades de dados diretamente. Espécies basais (Herrerasaurus, Staurikosaurus, Saturnalia, Coelophysis...) ficam em clados mais altos, o que é fiel à incerteza filogenética real; o Nyasasaurus, que pode nem ser dinossauro, fica na própria raiz.

A escala de tempo usa **indivíduos** ligados por `subperiodoDe` (transitiva): `JurassicoSuperior subperiodoDe Jurassico subperiodoDe Mesozoico`. As espécies declaram só a época (`viveuEm JurassicoSuperior`); período e era são inferidos. Datas em milhões de anos atrás (Ma), segundo a ICS 2023:

| Intervalo | Nível | Início (Ma) | Fim (Ma) |
|---|---|---|---|
| Mesozoico | Era | 251,9 | 66,0 |
| Triássico | Período | 251,9 | 201,4 |
| Jurássico | Período | 201,4 | 143,1 |
| Cretáceo | Período | 143,1 | 66,0 |
| Triássico Médio | Época | 247,2 | 237,0 |
| Triássico Superior | Época | 237,0 | 201,4 |
| Jurássico Inferior | Época | 201,4 | 174,7 |
| Jurássico Médio | Época | 174,7 | 161,5 |
| Jurássico Superior | Época | 161,5 | 143,1 |
| Cretáceo Inferior | Época | 143,1 | 100,5 |
| Cretáceo Superior | Época | 100,5 | 66,0 |

## Propriedades

| Objeto | Domain → Range | | Dados | Domain → Range |
|---|---|---|---|---|
| `viveuEm` | Dinossauro → IntervaloGeologico | | `nomeCientifico` | Dinossauro → xsd:string |
| `subperiodoDe` / `temSubperiodo` | Intervalo → Intervalo | | `comprimentoMetros` | Dinossauro → xsd:decimal |
| `encontradoEm` | Dinossauro → FormacaoGeologica | | `massaToneladas` | Dinossauro → xsd:decimal |
| `localizadaEm` | FormacaoGeologica → Pais | | `anoDescricao` | Dinossauro → xsd:integer |
| `formacaoDatadaEm` | FormacaoGeologica → Intervalo | | `dieta` | Dinossauro → xsd:string |
| `descritoPor` / `descreveu` | Dinossauro ↔ Paleontologo | | `inicioMa` | Intervalo → xsd:decimal |
| `predouSobre` / `presaDe` | Theropoda ↔ Dinossauro | | `fimMa` | Intervalo → xsd:decimal |

Em RDFS, domain e range são **regras de inferência, não validação**: quem é sujeito de `viveuEm` passa a ser Dinossauro. Validar dados exigiria SHACL, fora do escopo do trabalho.

## Construções OWL e justificativa

| Construção | Onde | Por quê (no domínio) |
|---|---|---|
| `owl:TransitiveProperty` | `subperiodoDe` | Jurássico Superior ⊂ Jurássico ⊂ Mesozoico implica Jurássico Superior ⊂ Mesozoico. |
| `owl:propertyChainAxiom` | `viveuEm ∘ subperiodoDe → viveuEm` | Quem viveu numa época viveu no período e na era que a contêm. Torna `viveuEm` "transitiva ao longo da escala" sem violar domain/range (Dinossauro → Intervalo). |
| `owl:inverseOf` | `temSubperiodo`, `descreveu`, `presaDe` | Permite navegar as relações nos dois sentidos (era → épocas, paleontólogo → espécies, presa → predador). |
| `owl:FunctionalProperty` | `nomeCientifico`, `anoDescricao`, `localizadaEm`, `inicioMa`, `fimMa` | Uma espécie tem um único nome válido e um ano de descrição; um intervalo tem um único início/fim; cada formação pertence a um único país. |
| `owl:AsymmetricProperty` | `predouSobre` | Predação documentada é de mão única entre as espécies da base. |
| `owl:disjointWith` | Saurischia x Ornithischia | As duas linhagens fundamentais de Dinosauria não se sobrepõem. |
| `owl:AllDisjointClasses` | Era, Periodo, Epoca | Um intervalo ocupa um único nível da escala. |
| `owl:equivalentClass` + `owl:Restriction` | `Predador ≡ ∃ predouSobre.Dinossauro` | Classe definida: ninguém é declarado Predador; um raciocinador classifica como Predador quem tem predação registrada. |

**Por que cadeia de propriedades e não `viveuEm` transitiva:** se `viveuEm` fosse transitiva, ela também valeria entre intervalos, e o domain Dinossauro faria um raciocinador concluir que o Jurássico é um dinossauro. A cadeia `viveuEm ∘ subperiodoDe → viveuEm` sempre começa num dinossauro, então só produz conclusões corretas.

## Consultas

### Parte 1, `g.triples()`

Cada consulta tem comentários `Busca:` e `Esperado:` no código (`consultas.py`, função `parte1`).

| # | Padrão | Propósito | Resultado real |
|---|---|---|---|
| 1.1 | `(S, None, None)` | Ficha completa do T. rex | 13 fatos: Tyrannosauridae, 12,3 m, 8,4 t, 1905, carnívoro, Cretáceo Superior, Hell Creek, Osborn, 3 presas |
| 1.2 | `(None, P, None)` | Espécie → formação onde foi encontrada | 63 pares, um por espécie |
| 1.3 | `(None, None, O)` | Tudo que referencia o Cretáceo Superior | 26 espécies via `viveuEm` + 13 formações via `formacaoDatadaEm` |
| 1.4 | `(S, P, None)` em laço | Linhagem de Tyrannosauridae até Dinossauro | Tyrannosauridae › Coelurosauria › Theropoda › Saurischia › Dinossauro |
| 1.5 | `(None, P, O)` | Espécies descritas por Othniel Marsh | 8 espécies, de Allosaurus e Apatosaurus (1877) a Edmontosaurus (1892) |
| 1.6 | `(None, rdf:type, O)` | Propriedades transitivas e funcionais da ontologia | transitiva: `subperiodoDe`; funcionais: as 5 |
| 1.7 | `(S, P, O) in g` | Verificação de fatos pontuais | Spinosaurus viveu no Cretáceo Superior: `True`; T. rex no Jurássico Superior: `False` |

Exemplo de comentário e de laço (1.4), subindo a hierarquia sem SPARQL:

```python
# 1.4 Sujeito e predicado fixos (S, P, None).
# Busca: a cadeia de superclasses de Tyrannosauridae, subindo um nivel
# por vez com (classe, rdfs:subClassOf, None).
# Esperado: Tyrannosauridae > Coelurosauria > Theropoda > Saurischia > Dinossauro.
cadeia, atual = [DINO.Tyrannosauridae], DINO.Tyrannosauridae
while True:
    superclasses = [o for _, _, o in g.triples((atual, RDFS.subClassOf, None))]
    if not superclasses:
        break
    atual = superclasses[0]
    cadeia.append(atual)
```

### Parte 2, SPARQL

| # | Tipo | Propósito | Resultado real |
|---|---|---|---|
| 2.1 | SELECT + FILTER + ORDER BY | Terópodes com mais de 8 m, do maior ao menor | 10 espécies: Spinosaurus 14,0 · Giganotosaurus 12,5 · T. rex 12,3 · ... · Allosaurus 8,5 |
| 2.2 | SELECT + COUNT/AVG/MAX + GROUP BY | Espécies e massa por período (usa transitividade) | Triássico 9 · Jurássico 16 · Cretáceo 38 |
| 2.3 | SELECT + subconsulta + GROUP_CONCAT | Linhagem completa das espécies brasileiras | Austroposeidon: Dinossauro > Saurischia > Sauropodomorpha > Sauropoda > Titanosauria (e mais 7) |
| 2.4 | SELECT + UNION | Cadeia alimentar considerando a propriedade inversa | 7 relações, com razão de massa; Deinonychus → Tenontosaurus vem só da inversa `presaDe` |
| 2.5 | SELECT + HAVING | Paleontólogos com mais de uma espécie descrita | 13 nomes: Marsh 8 (1877–1892) · Osborn 5 · Coria 3 · Lambe 3 · ... |
| 2.6 | ASK | T. rex e Stegosaurus coexistiram? | `false` (Cretáceo vs Jurássico) |
| 2.7 | ASK | Existe dinossauro brasileiro do Triássico? | `true` (5 espécies, formações Santa Maria e Caturrita) |
| 2.8 | CONSTRUCT | Materializa `viveuEm` para época, período e era | 51 triplas (17 ornitísquios × época, período, Mesozoico) |
| 2.9 | INSERT DATA | Adiciona Oxalaia quilombensis (Brasil, 2011) | Spinosauridae: 2 → 3 espécies, +16 triplas |
| 2.10 | DELETE/INSERT | Dieta dos Spinosauridae vira "piscivoro" (Ibrahim et al. 2014, 2020) | Irritator, Oxalaia, Spinosaurus: carnivoro → piscivoro |
| 2.11 | DELETE DATA | Remove predação T. rex → Ankylosaurus, sem evidência fóssil | presas do T. rex: 3 → 2, −1 tripla |

<details>
<summary>2.2 completa: consulta e saída</summary>

```sparql
SELECT ?periodo (COUNT(?d) AS ?especies)
       (ROUND(AVG(?m) * 10) / 10 AS ?massaMedia) (MAX(?m) AS ?massaMax)
WHERE { ?d dino:viveuEm/dino:subperiodoDe* ?p ; dino:massaToneladas ?m .
        ?p a dino:Periodo ; rdfs:label ?periodo ; dino:inicioMa ?inicio . }
GROUP BY ?periodo ?inicio ORDER BY DESC(?inicio)
```

| Período | Espécies | Massa média (t) | Massa máx. (t) |
|---|---|---|---|
| Triássico | 9 | 0,2 | 0,9 |
| Jurássico | 16 | 8,3 | 35,0 |
| Cretáceo | 38 | 6,9 | 70,0 |

Nenhuma espécie declara `viveuEm Cretaceo` diretamente; a contagem por período só funciona porque `subperiodoDe*` sobe da época ao período.

</details>

<details>
<summary>2.4 completa: UNION para compensar a inversa</summary>

```sparql
SELECT ?predador ?presa (ROUND(?mp / ?mq * 100) / 100 AS ?razaoMassa) WHERE {
    { ?a dino:predouSobre ?b } UNION { ?b dino:presaDe ?a }
    ?a dino:nomeCientifico ?predador ; dino:massaToneladas ?mp .
    ?b dino:nomeCientifico ?presa ; dino:massaToneladas ?mq .
}
ORDER BY ?predador ?presa
```

| Predador | Presa | Razão de massa |
|---|---|---|
| Allosaurus | Stegosaurus | 0,34 |
| Deinonychus | Tenontosaurus | 0,07 |
| Majungasaurus | Rapetosaurus | 0,11 |
| T. rex | Ankylosaurus | 1,4 |
| T. rex | Edmontosaurus | 1,4 |
| T. rex | Triceratops | 0,93 |
| Velociraptor | Protoceratops | 0,19 |

</details>

<details>
<summary>2.8 CONSTRUCT e 2.10 DELETE/INSERT</summary>

```sparql
CONSTRUCT { ?d dino:viveuEm ?intervalo }
WHERE { ?d dino:viveuEm/dino:subperiodoDe* ?intervalo .
        ?d a/rdfs:subClassOf* dino:Ornithischia . }
```

```sparql
DELETE { ?d dino:dieta ?antiga }
INSERT { ?d dino:dieta "piscivoro" }
WHERE {
    ?d a/rdfs:subClassOf* dino:Spinosauridae ;
       dino:dieta ?antiga .
}
```

O 2.10 também altera o Oxalaia inserido no 2.9, porque o `WHERE` pega qualquer espécie do clado.

</details>

Cada update imprime o estado **antes e depois** e a variação no número de triplas. A última linha da saída resume: **1169 triplas no início, 1184 após os updates**. Os updates atuam só no grafo em memória; o `.ttl` não é alterado, então a execução é reproduzível.

## O rdflib não raciocina: como as consultas compensam

O rdflib guarda e consulta triplas, mas não aplica as regras de RDFS e OWL sozinho. Cada regra é reproduzida no padrão da consulta:

| Regra da ontologia | O que um raciocinador faria | Como a consulta compensa | Usado em |
|---|---|---|---|
| `rdfs:subClassOf` | T. rex também é Theropoda e Dinossauro | `rdf:type/rdfs:subClassOf*` | 2.1, 2.3, 2.8, 2.10 |
| `subperiodoDe` transitiva + cadeia em `viveuEm` | T. rex viveu no Cretáceo e no Mesozoico | `viveuEm/subperiodoDe*` | 2.2, 2.6, 2.7, 2.8 |
| `owl:inverseOf` | `presaDe` gera o `predouSobre` correspondente | `UNION` com a propriedade inversa | 2.4 |
| Inferências em geral | triplas novas no grafo | `CONSTRUCT` que materializa o resultado | 2.8 |

Os axiomas OWL continuam úteis: documentam o significado e valem sem mudanças para qualquer raciocinador OWL.

## Como executar

Requer Python 3.10+.

```bash
git clone <url-do-repositorio>
cd dino-taxo
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python consultas.py
```

A saída lista cada consulta com número e propósito, por exemplo `[2.6] ASK: T. rex e Stegosaurus coexistiram no mesmo periodo?`.

### Demo interativa no navegador

`demo.html` roda SPARQL de verdade sobre o `dinossauros.ttl` no navegador (motor [Oxigraph](https://github.com/oxigraph/oxigraph), carregado da internet). Tem um editor para consultas livres e as 11 consultas da Parte 2 em botões, com antes/depois nos updates e um botão para restaurar a base.

```bash
python3 -m http.server     # na pasta do projeto
# abra http://localhost:8000/demo.html
```

Diferença em relação ao `consultas.py`: na 2.4, a razão de massa é calculada em `xsd:double`, porque o Oxigraph perde precisão nessa conta com `xsd:decimal`. Os resultados são os mesmos.

### Guia de campo

`guide.html` mostra a base como um catálogo de fichas, uma por espécie, numeradas da mais antiga para a mais recente. Cada ficha é montada com consultas SPARQL (também via Oxigraph) e traz linhagem por clados, comprimento comparado a um humano, massa em escala logarítmica, a época numa linha do tempo do Mesozoico, formação, país, quem descreveu e quando, além de links para presas, predadores e espécies da mesma formação ou época. Dá para buscar pelo nome, filtrar por grupo, período ou espécies brasileiras, e navegar com as setas do teclado. O link `guide.html#Irritator` abre direto na ficha da espécie.

Sirva a pasta do mesmo jeito e abra `http://localhost:8000/guide.html`.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `dinossauros.ttl` | Ontologia (classes, propriedades, axiomas OWL) e indivíduos |
| `consultas.py` | Carrega o `.ttl` e executa todas as consultas |
| `demo.html` | Demo interativa: editor SPARQL e consultas prontas no navegador |
| `guide.html` | Guia de campo: uma ficha por espécie, com busca e filtros |
| `requirements.txt` | Dependência (`rdflib`) |
| `Mini_Projeto_03_-_Roteiro.pdf` | Enunciado do projeto |

## Fontes dos dados

Datas da escala de tempo: International Chronostratigraphic Chart (ICS, 2023). Medidas, anos e autores das descrições: literatura paleontológica de referência (valores médios das estimativas publicadas).
