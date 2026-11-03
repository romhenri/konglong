"""Mini-Projeto 3: consultas rdflib e SPARQL sobre a base dinossauros.ttl."""

from pathlib import Path

from rdflib import OWL, RDF, RDFS, Graph, Namespace

DINO = Namespace("http://example.org/dino#")
TTL = Path(__file__).with_name("dinossauros.ttl")

PREFIXOS = """
PREFIX dino: <http://example.org/dino#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""


def cabecalho(numero, proposito):
    print(f"\n{'=' * 72}\n[{numero}] {proposito}\n{'-' * 72}")


def nome(g, termo):
    """rdfs:label do termo, ou o nome local da URI, ou o literal."""
    rotulo = g.value(termo, RDFS.label)
    if rotulo is not None:
        return str(rotulo)
    return str(termo).split("#")[-1]


def imprimir_select(resultado):
    linhas = list(resultado)
    if not linhas:
        print("  (nenhum resultado)")
    for linha in linhas:
        print("  " + " | ".join("-" if v is None else str(v) for v in linha))
    print(f"  ({len(linhas)} linha(s))")


def estatisticas(g):
    """Confere os minimos exigidos pelo roteiro."""
    classes = set(g.subjects(RDF.type, OWL.Class))
    obj = set(g.subjects(RDF.type, OWL.ObjectProperty))
    dados = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    individuos = {s for c in classes for s in g.subjects(RDF.type, c)}
    construcoes_owl = {
        "owl:TransitiveProperty": len(set(g.subjects(RDF.type, OWL.TransitiveProperty))),
        "owl:FunctionalProperty": len(set(g.subjects(RDF.type, OWL.FunctionalProperty))),
        "owl:AsymmetricProperty": len(set(g.subjects(RDF.type, OWL.AsymmetricProperty))),
        "owl:inverseOf": len(list(g.triples((None, OWL.inverseOf, None)))),
        "owl:propertyChainAxiom": len(list(g.triples((None, OWL.propertyChainAxiom, None)))),
        "owl:disjointWith": len(list(g.triples((None, OWL.disjointWith, None)))),
        "owl:AllDisjointClasses": len(set(g.subjects(RDF.type, OWL.AllDisjointClasses))),
        "owl:equivalentClass + owl:Restriction": len(list(g.triples((None, OWL.equivalentClass, None)))),
    }
    cabecalho("0", "Estatisticas da base x minimos do roteiro")
    for rotulo, valor, minimo in [
        ("Triplas", len(g), 50),
        ("Classes", len(classes), 8),
        ("Propriedades de objeto", len(obj), 5),
        ("Propriedades de dados", len(dados), 5),
        ("Individuos", len(individuos), 25),
        ("Tipos de construcao OWL", sum(1 for v in construcoes_owl.values() if v), 5),
    ]:
        print(f"  {rotulo:<26} {valor:>4}  (minimo {minimo}) {'OK' if valor >= minimo else 'FALTA'}")
    print("  Construcoes OWL usadas:")
    for k, v in construcoes_owl.items():
        print(f"    - {k}: {v}")


# =====================================================================
# PARTE 1: consultas com g.triples()
# =====================================================================

def parte1(g):
    # 1.1 Sujeito fixo (S, None, None).
    # Busca: todos os fatos sobre o Tyrannosaurus rex.
    # Esperado: tipo Tyrannosauridae, label, nome cientifico, medidas, ano 1905,
    # dieta, viveuEm Cretaceo Superior, Hell Creek, Osborn e 3 presas.
    cabecalho("1.1", "g.triples((T. rex, None, None)): ficha completa do T. rex")
    for _, p, o in g.triples((DINO.Tyrannosaurus_rex, None, None)):
        print(f"  {nome(g, p):<22} -> {nome(g, o)}")

    # 1.2 Predicado fixo (None, P, None).
    # Busca: em qual formacao geologica cada especie foi encontrada.
    # Esperado: 19 pares especie -> formacao (uma por especie).
    cabecalho("1.2", "g.triples((None, encontradoEm, None)): especie -> formacao")
    pares = sorted((nome(g, s), nome(g, o)) for s, _, o in g.triples((None, DINO.encontradoEm, None)))
    for s, o in pares:
        print(f"  {s:<18} -> {o}")
    print(f"  ({len(pares)} pares)")

    # 1.3 Objeto fixo (None, None, O).
    # Busca: tudo que aponta para o Cretaceo Superior, com qualquer predicado.
    # Esperado: especies (viveuEm), formacoes (formacaoDatadaEm) e nenhum
    # subperiodo (o Cretaceo Superior e uma folha da escala).
    cabecalho("1.3", "g.triples((None, None, CretaceoSuperior)): quem referencia o Cretaceo Superior")
    for s, p, _ in sorted(g.triples((None, None, DINO.CretaceoSuperior))):
        print(f"  {nome(g, s):<28} {nome(g, p)}")

    # 1.4 Sujeito e predicado fixos (S, P, None).
    # Busca: a cadeia de superclasses de Tyrannosauridae, subindo um nivel
    # por vez com (classe, rdfs:subClassOf, None).
    # Esperado: Tyrannosauridae > Theropoda > Saurischia > Dinossauro.
    cabecalho("1.4", "g.triples((classe, rdfs:subClassOf, None)) em laco: linhagem de Tyrannosauridae")
    cadeia, atual = [DINO.Tyrannosauridae], DINO.Tyrannosauridae
    while True:
        superclasses = [o for _, _, o in g.triples((atual, RDFS.subClassOf, None))]
        if not superclasses:
            break
        atual = superclasses[0]
        cadeia.append(atual)
    print("  " + " > ".join(nome(g, c) for c in cadeia))

    # 1.5 Predicado e objeto fixos (None, P, O).
    # Busca: especies descritas por Othniel Marsh (protagonista da "Guerra
    # dos Ossos").
    # Esperado: Allosaurus, Diplodocus, Stegosaurus, Triceratops, Edmontosaurus.
    cabecalho("1.5", "g.triples((None, descritoPor, OthnielMarsh)): especies descritas por Marsh")
    for s, _, _ in sorted(g.triples((None, DINO.descritoPor, DINO.OthnielMarsh))):
        print(f"  {g.value(s, DINO.nomeCientifico)} ({g.value(s, DINO.anoDescricao)})")

    # 1.6 Predicado e objeto fixos sobre o esquema (None, rdf:type, X).
    # Busca: propriedades declaradas transitivas e funcionais na ontologia.
    # Esperado: transitiva = subperiodoDe; funcionais = localizadaEm,
    # nomeCientifico, anoDescricao, inicioMa, fimMa.
    cabecalho("1.6", "g.triples((None, rdf:type, owl:Transitive/FunctionalProperty)): semantica OWL declarada")
    for tipo in (OWL.TransitiveProperty, OWL.FunctionalProperty):
        props = sorted(nome(g, s) for s, _, _ in g.triples((None, RDF.type, tipo)))
        print(f"  {tipo.split('#')[-1]}: {', '.join(props)}")

    # 1.7 Tripla totalmente fixa (S, P, O) via operador `in`.
    # Busca: verificar fatos pontuais.
    # Esperado: Spinosaurus viveu no Cretaceo Superior = True;
    # T. rex viveu no Jurassico Superior = False.
    cabecalho("1.7", "(S, P, O) in g: verificacao de fatos pontuais")
    for tripla in [
        (DINO.Spinosaurus_aegyptiacus, DINO.viveuEm, DINO.CretaceoSuperior),
        (DINO.Tyrannosaurus_rex, DINO.viveuEm, DINO.JurassicoSuperior),
    ]:
        print(f"  {nome(g, tripla[0])} viveuEm {nome(g, tripla[2])}? {tripla in g}")


# =====================================================================
# PARTE 2: consultas SPARQL
# =====================================================================

# Padrao recorrente: "?x rdf:type/rdfs:subClassOf* dino:Theropoda" faz a
# inferencia de subclasse que o rdflib sozinho nao faz; e
# "dino:viveuEm/dino:subperiodoDe*" aplica a transitividade de
# subperiodoDe (e a cadeia de propriedades declarada em viveuEm).

S1 = """
# Teropodes com mais de 8 m, do maior para o menor (FILTER + ORDER BY).
SELECT ?nome ?clado ?comprimento ?massa WHERE {
    ?d rdf:type ?c ;
       dino:nomeCientifico ?nome ;
       dino:comprimentoMetros ?comprimento ;
       dino:massaToneladas ?massa .
    ?c rdfs:subClassOf* dino:Theropoda ;
       rdfs:label ?clado .
    FILTER (?comprimento > 8)
}
ORDER BY DESC(?comprimento)
"""

S2 = """
# Especies por periodo geologico, com massa media e a maior especie
# (agregacao + transitividade: as especies apontam para epocas, e o
# periodo e alcancado por subperiodoDe*).
SELECT ?periodo (COUNT(?d) AS ?especies) (ROUND(AVG(?m) * 10) / 10 AS ?massaMedia) (MAX(?m) AS ?massaMax)
WHERE {
    ?d dino:viveuEm/dino:subperiodoDe* ?p ;
       dino:massaToneladas ?m .
    ?p a dino:Periodo ;
       rdfs:label ?periodo ;
       dino:inicioMa ?inicio .
}
GROUP BY ?periodo ?inicio
ORDER BY DESC(?inicio)
"""

S3 = """
# Linhagem completa de cada especie brasileira: todos os clados acima da
# classe direta, ate Dinossauro (taxonomia profunda via subClassOf*).
# A subconsulta calcula a profundidade de cada clado para que o
# GROUP_CONCAT saia ordenado da raiz para a folha.
SELECT ?nome ?formacao (GROUP_CONCAT(?cladoNome; separator=" > ") AS ?linhagem)
WHERE {
    {
        SELECT ?nome ?formacao ?cladoNome (COUNT(?sup) AS ?profundidade) WHERE {
            ?d dino:encontradoEm ?f ;
               dino:nomeCientifico ?nome ;
               rdf:type/rdfs:subClassOf* ?clado .
            ?f dino:localizadaEm dino:Brasil ;
               rdfs:label ?formacao .
            ?clado rdfs:label ?cladoNome ;
                   rdfs:subClassOf* ?sup .
            ?sup rdfs:subClassOf* dino:Dinossauro .
        }
        GROUP BY ?nome ?formacao ?cladoNome
        ORDER BY ?nome ?profundidade
    }
}
GROUP BY ?nome ?formacao
ORDER BY ?nome
"""

S4 = """
# Relacoes predador-presa, aceitando o fato declarado em qualquer uma
# das direcoes (predouSobre ou sua inversa presaDe), ja que o rdflib nao
# materializa owl:inverseOf. Mostra tambem a razao de massa.
SELECT ?predador ?presa (ROUND(?mp / ?mq * 100) / 100 AS ?razaoMassa) WHERE {
    { ?a dino:predouSobre ?b } UNION { ?b dino:presaDe ?a }
    ?a dino:nomeCientifico ?predador ; dino:massaToneladas ?mp .
    ?b dino:nomeCientifico ?presa ; dino:massaToneladas ?mq .
}
ORDER BY ?predador ?presa
"""

S5 = """
# Paleontologos com mais de uma especie descrita (agregacao + HAVING),
# com o intervalo de anos das descricoes.
SELECT ?paleontologo (COUNT(?d) AS ?especies) (MIN(?ano) AS ?primeira) (MAX(?ano) AS ?ultima)
WHERE {
    ?d dino:descritoPor ?p ; dino:anoDescricao ?ano .
    ?p rdfs:label ?paleontologo .
}
GROUP BY ?paleontologo
HAVING (COUNT(?d) > 1)
ORDER BY DESC(?especies)
"""

A1 = """
# T. rex e Stegosaurus compartilharam algum periodo geologico?
# Esperado: false (Cretaceo vs Jurassico; ~80 milhoes de anos de distancia).
ASK {
    dino:Tyrannosaurus_rex   dino:viveuEm/dino:subperiodoDe* ?p .
    dino:Stegosaurus_stenops dino:viveuEm/dino:subperiodoDe* ?p .
    ?p a dino:Periodo .
}
"""

A2 = """
# Existe algum dinossauro brasileiro do Triassico (um dos mais antigos)?
# Esperado: true (Staurikosaurus e Saturnalia, Formacao Santa Maria).
ASK {
    ?d dino:encontradoEm/dino:localizadaEm dino:Brasil ;
       dino:viveuEm/dino:subperiodoDe* dino:Triassico .
}
"""

C1 = """
# Materializa a cadeia owl:propertyChainAxiom de viveuEm:
# para cada especie, gera viveuEm para TODOS os intervalos que contem a
# epoca declarada (epoca, periodo e era).
CONSTRUCT { ?d dino:viveuEm ?intervalo }
WHERE {
    ?d dino:viveuEm/dino:subperiodoDe* ?intervalo .
    ?d a/rdfs:subClassOf* dino:Ornithischia .
}
"""

CONTAGEM_SPINO = """
SELECT ?nome ?dieta ?formacao WHERE {
    ?d a/rdfs:subClassOf* dino:Spinosauridae ;
       dino:nomeCientifico ?nome ; dino:dieta ?dieta ;
       dino:encontradoEm/rdfs:label ?formacao .
}
ORDER BY ?nome
"""

U1 = """
# INSERT: registra Oxalaia quilombensis (Kellner et al., 2011), o maior
# espinossaurideo do Brasil, e a Formacao Alcantara (MA) onde foi achado.
INSERT DATA {
    dino:Alcantara a dino:FormacaoGeologica ;
        rdfs:label "Formacao Alcantara"@pt ;
        dino:localizadaEm dino:Brasil ;
        dino:formacaoDatadaEm dino:CretaceoSuperior .
    dino:AlexanderKellner a dino:Paleontologo ; rdfs:label "Alexander Kellner"@pt .
    dino:Oxalaia_quilombensis a dino:Spinosauridae ;
        rdfs:label "Oxalaia"@pt ;
        dino:nomeCientifico "Oxalaia quilombensis" ;
        dino:comprimentoMetros 12.0 ; dino:massaToneladas 5.0 ;
        dino:anoDescricao 2011 ; dino:dieta "carnivoro" ;
        dino:viveuEm dino:CretaceoSuperior ;
        dino:encontradoEm dino:Alcantara ;
        dino:descritoPor dino:AlexanderKellner .
}
"""

U2 = """
# DELETE/INSERT: estudos de Ibrahim et al. (2014, 2020) indicam que
# espinossaurideos eram especializados em peixes. Troca a dieta de TODOS
# os Spinosauridae (inclusive o Oxalaia recem-inserido) para "piscivoro".
DELETE { ?d dino:dieta ?antiga }
INSERT { ?d dino:dieta "piscivoro" }
WHERE {
    ?d a/rdfs:subClassOf* dino:Spinosauridae ;
       dino:dieta ?antiga .
}
"""

PREDACAO_TREX = """
SELECT ?presa WHERE { dino:Tyrannosaurus_rex dino:predouSobre/dino:nomeCientifico ?presa }
ORDER BY ?presa
"""

U3 = """
# DELETE: remove a predacao T. rex -> Ankylosaurus, por nao haver
# evidencia fossil direta (marca de mordida ou conteudo estomacal);
# a base so deve conter predacoes documentadas.
DELETE DATA {
    dino:Tyrannosaurus_rex dino:predouSobre dino:Ankylosaurus_magniventris .
}
"""


def parte2(g):
    q = lambda texto: g.query(PREFIXOS + texto)  # noqa: E731

    cabecalho("2.1", "SELECT + FILTER + ORDER BY: teropodes com mais de 8 m")
    imprimir_select(q(S1))

    cabecalho("2.2", "SELECT + agregacao (COUNT/AVG/MAX) + transitividade: especies por periodo")
    imprimir_select(q(S2))

    cabecalho("2.3", "SELECT + GROUP_CONCAT + subClassOf*: linhagem das especies brasileiras")
    imprimir_select(q(S3))

    cabecalho("2.4", "SELECT + UNION (inversa): cadeia alimentar documentada")
    imprimir_select(q(S4))

    cabecalho("2.5", "SELECT + GROUP BY + HAVING: paleontologos mais produtivos")
    imprimir_select(q(S5))

    cabecalho("2.6", "ASK: T. rex e Stegosaurus coexistiram no mesmo periodo?")
    print(f"  {q(A1).askAnswer}")

    cabecalho("2.7", "ASK: existe dinossauro brasileiro do Triassico?")
    print(f"  {q(A2).askAnswer}")

    cabecalho("2.8", "CONSTRUCT: materializa viveuEm transitivo (epoca -> periodo -> era) dos ornitisquios")
    derivado = q(C1).graph
    derivado.bind("dino", DINO)
    print("  " + derivado.serialize(format="turtle").strip().replace("\n", "\n  "))
    print(f"  ({len(derivado)} triplas derivadas; o .ttl declara apenas a epoca de cada especie)")

    total_antes = len(g)
    cabecalho("2.9", "UPDATE INSERT DATA: adiciona Oxalaia quilombensis (Brasil, 2011)")
    print("  ANTES (Spinosauridae):")
    imprimir_select(q(CONTAGEM_SPINO))
    g.update(PREFIXOS + U1)
    print(f"  DEPOIS (Spinosauridae): {len(g) - total_antes:+d} triplas")
    imprimir_select(q(CONTAGEM_SPINO))

    cabecalho("2.10", "UPDATE DELETE/INSERT: dieta dos Spinosauridae passa a 'piscivoro'")
    print("  ANTES:")
    imprimir_select(q(CONTAGEM_SPINO))
    g.update(PREFIXOS + U2)
    print("  DEPOIS:")
    imprimir_select(q(CONTAGEM_SPINO))

    cabecalho("2.11", "UPDATE DELETE DATA: remove predacao T. rex -> Ankylosaurus (sem evidencia)")
    print("  ANTES (presas do T. rex):")
    imprimir_select(q(PREDACAO_TREX))
    antes = len(g)
    g.update(PREFIXOS + U3)
    print(f"  DEPOIS (presas do T. rex): {len(g) - antes:+d} tripla")
    imprimir_select(q(PREDACAO_TREX))

    print(f"\n  Triplas no grafo: {total_antes} no inicio, {len(g)} apos os updates "
          "(o arquivo .ttl nao e alterado).")


if __name__ == "__main__":
    grafo = Graph().parse(TTL, format="turtle")
    estatisticas(grafo)
    print("\n\n######## PARTE 1: consultas com g.triples() ########")
    parte1(grafo)
    print("\n\n######## PARTE 2: consultas SPARQL ########")
    parte2(grafo)
