# Dinossauros e Clados: base de conhecimento RDF/OWL

Mini-Projeto 3: base de conhecimento modelada com RDF, RDFS e OWL em Turtle (`dinossauros.ttl`) e consultada com rdflib e SPARQL (`consultas.py`).

## Resumo da base

A base descreve **19 espécies de dinossauros** reais, classificadas por **clados** (Saurischia, Theropoda, Ceratopsia...), situadas na **escala de tempo geológico** (Era > Período > Época), ligadas às **formações geológicas** e aos **países** onde foram encontradas, e aos **paleontólogos** que as descreveram. Também registra relações de **predação** com evidência fóssil (ex.: os "Dinossauros Lutadores", Velociraptor x Protoceratops).

| Item | Quantidade | Mínimo |
|---|---|---|
| Triplas | 495 | 50 |
| Classes | 23 | 8 |
| Propriedades de objeto | 10 | 5 |
| Propriedades de dados | 7 | 5 |
| Indivíduos | 58 | 25 |
| Tipos de construção OWL | 8 | 5 |

Esses números são recalculados e impressos pela própria aplicação (consulta `[0]`).

## Taxonomia (hierarquia de classes)

A taxonomia de dinossauros é naturalmente profunda: chega a **3 níveis abaixo da raiz** `Dinossauro`.

```
Dinossauro
├── Saurischia            (quadril de lagarto)
│   ├── Theropoda         (bípedes, maioria carnívora)
│   │   ├── Tyrannosauridae     Tyrannosaurus rex
│   │   ├── Dromaeosauridae     Velociraptor, Deinonychus
│   │   ├── Spinosauridae       Spinosaurus, Irritator (BR)
│   │   └── Allosauroidea       Allosaurus, Giganotosaurus
│   ├── Sauropodomorpha         Saturnalia (BR)
│   │   └── Sauropoda           Brachiosaurus, Diplodocus, Argentinosaurus
│   └── (basais)                Herrerasaurus, Staurikosaurus (BR)
├── Ornithischia          (quadril de ave)
│   ├── Ornithopoda             Edmontosaurus, Iguanodon
│   ├── Ceratopsia              Triceratops, Protoceratops
│   └── Thyreophora
│       ├── Stegosauria         Stegosaurus
│       └── Ankylosauria        Ankylosaurus
└── Predador              (classe definida por restrição OWL)

IntervaloGeologico
├── Era        Mesozoico
├── Periodo    Triassico, Jurassico, Cretaceo
└── Epoca      Triassico Superior, Jurassico Superior, Cretaceo Inferior, Cretaceo Superior

FormacaoGeologica   Hell Creek, Morrison, Santa Maria, Romualdo, ... (11)
Pais                Brasil, Argentina, EUA, Mongolia, Egito, Belgica
Paleontologo        Marsh, Osborn, Coria, Langer, ... (14)
```

**Decisão de modelagem:** clados são **classes** e espécies são **indivíduos** do clado mais específico conhecido. Assim, `Tyrannosaurus_rex a Tyrannosauridae` basta; a pertinência a Theropoda, Saurischia e Dinossauro decorre de `rdfs:subClassOf` e é recuperada nas consultas com o caminho SPARQL `rdf:type/rdfs:subClassOf*`. Espécies basais (Herrerasaurus, Staurikosaurus, Saturnalia) ficam em clados mais altos, o que é fiel à incerteza filogenética real.

A escala de tempo usa **indivíduos** ligados por `subperiodoDe` (transitiva): `JurassicoSuperior subperiodoDe Jurassico subperiodoDe Mesozoico`. As espécies declaram só a época (`viveuEm JurassicoSuperior`); período e era são inferidos.

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
| `owl:equivalentClass` + `owl:Restriction` | `Predador ≡ ∃ predouSobre.Dinossauro` | Classe definida: um raciocinador classifica como Predador quem tem predação registrada. |

O rdflib não faz raciocínio OWL. Por isso as consultas aplicam a semântica explicitamente: `subClassOf*` para herança, `viveuEm/subperiodoDe*` para a transitividade e `UNION` com a propriedade inversa para predação. A consulta CONSTRUCT 2.8 materializa as triplas que a cadeia de propriedades inferiria.

## Consultas

**Parte 1, `g.triples()`** (cada uma comentada no código com o que busca e o resultado esperado):

| # | Padrão | Propósito |
|---|---|---|
| 1.1 | `(S, None, None)` | Ficha completa do T. rex |
| 1.2 | `(None, P, None)` | Espécie → formação onde foi encontrada |
| 1.3 | `(None, None, O)` | Tudo que referencia o Cretáceo Superior |
| 1.4 | `(S, P, None)` em laço | Linhagem de Tyrannosauridae até Dinossauro |
| 1.5 | `(None, P, O)` | Espécies descritas por Othniel Marsh |
| 1.6 | `(None, rdf:type, O)` | Propriedades transitivas e funcionais da ontologia |
| 1.7 | `(S, P, O) in g` | Verificação de fatos pontuais |

**Parte 2, SPARQL:**

| # | Tipo | Propósito |
|---|---|---|
| 2.1 | SELECT + FILTER + ORDER BY | Terópodes com mais de 8 m, do maior ao menor |
| 2.2 | SELECT + COUNT/AVG/MAX + GROUP BY | Espécies e massa por período (usa transitividade) |
| 2.3 | SELECT + subconsulta + GROUP_CONCAT | Linhagem completa das espécies brasileiras |
| 2.4 | SELECT + UNION | Cadeia alimentar considerando a propriedade inversa |
| 2.5 | SELECT + HAVING | Paleontólogos com mais de uma espécie descrita |
| 2.6 | ASK | T. rex e Stegosaurus coexistiram? (`false`) |
| 2.7 | ASK | Existe dinossauro brasileiro do Triássico? (`true`) |
| 2.8 | CONSTRUCT | Materializa `viveuEm` para época, período e era |
| 2.9 | INSERT DATA | Adiciona Oxalaia quilombensis (Brasil, 2011) |
| 2.10 | DELETE/INSERT | Dieta dos Spinosauridae vira "piscivoro" (Ibrahim et al. 2014, 2020) |
| 2.11 | DELETE DATA | Remove predação T. rex → Ankylosaurus, sem evidência fóssil |

Cada update imprime o estado **antes e depois** e a variação no número de triplas. Os updates atuam só no grafo em memória; o `.ttl` não é alterado, então a execução é reproduzível.

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

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `dinossauros.ttl` | Ontologia (classes, propriedades, axiomas OWL) e indivíduos |
| `consultas.py` | Carrega o `.ttl` e executa todas as consultas |
| `requirements.txt` | Dependência (`rdflib`) |
| `Mini_Projeto_03_-_Roteiro.pdf` | Enunciado do projeto |

## Fontes dos dados

Datas da escala de tempo: International Chronostratigraphic Chart (ICS, 2023). Medidas, anos e autores das descrições: literatura paleontológica de referência (valores médios das estimativas publicadas).
