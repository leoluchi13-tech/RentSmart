import csv
from dataclasses import dataclass
from pathlib import Path


def valor_decimal(centavos: int) -> str:
    inteiro, fracao = divmod(centavos, 100)
    return f"{inteiro},{fracao:02d}"


def brl(centavos: int) -> str:
    inteiro, fracao = divmod(centavos, 100)
    milhares = f"{inteiro:,}".replace(",", ".")
    return f"R$ {milhares},{fracao:02d}"


@dataclass(frozen=True)
class Imovel:
    nome: str
    aluguel_base: int
    adicional_segundo_quarto: int = 0

    def adicionais(self, quartos: int, vagas: int) -> tuple[int, int]:
        if self.nome == "Estúdio":
            estacionamento = 25_000 + (vagas - 2) * 6_000 if vagas else 0
            return 0, estacionamento

        quartos_extra = self.adicional_segundo_quarto if quartos == 2 else 0
        return quartos_extra, vagas * 30_000

    def desconto(self, subtotal: int, tem_criancas: bool) -> int:
        if self.nome == "Apartamento" and not tem_criancas:
            return (subtotal * 5 + 50) // 100
        return 0


IMOVEIS = {
    1: Imovel("Apartamento", 70_000, 20_000),
    2: Imovel("Casa", 90_000, 25_000),
    3: Imovel("Estúdio", 120_000),
}


@dataclass(frozen=True)
class Orcamento:
    imovel: Imovel
    quartos: int
    vagas: int
    tem_criancas: bool
    parcelas: int

    TAXA_CONTRATUAL = 200_000

    def detalhar_aluguel(self) -> dict[str, int]:
        base = self.imovel.aluguel_base
        quartos, garagem = self.imovel.adicionais(self.quartos, self.vagas)
        subtotal = base + quartos + garagem
        desconto = self.imovel.desconto(subtotal, self.tem_criancas)
        return {
            "Aluguel-base": base,
            "Adicional de quarto": quartos,
            "Estacionamento": garagem,
            "Subtotal mensal": subtotal,
            "Desconto mensal": desconto,
            "Aluguel mensal": subtotal - desconto,
        }

    def parcelas_contrato(self) -> list[int]:
        valor, sobra = divmod(self.TAXA_CONTRATUAL, self.parcelas)
        return [valor] * (self.parcelas - 1) + [valor + sobra]

    def projetar(self) -> list[tuple[int, int, int, int]]:
        aluguel = self.detalhar_aluguel()["Aluguel mensal"]
        parcelas = self.parcelas_contrato()
        linhas = []
        for mes in range(1, 13):
            taxa = parcelas[mes - 1] if mes <= len(parcelas) else 0
            linhas.append((mes, aluguel, taxa, aluguel + taxa))
        return linhas


def ler_inteiro(pergunta: str, minimo: int, maximo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(pergunta))
            if valor >= minimo and (maximo is None or valor <= maximo):
                return valor
        except ValueError:
            pass
        intervalo = f"de {minimo} a {maximo}" if maximo is not None else f"a partir de {minimo}"
        print(f"Digite um número inteiro {intervalo}.")


def ler_sim_nao(pergunta: str) -> bool:
    while True:
        resposta = input(pergunta).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Digite S para sim ou N para não.")


def coletar_orcamento() -> Orcamento:
    print("RentSmart | R.M Imóveis")
    print("1. Apartamento\n2. Casa\n3. Estúdio")
    imovel = IMOVEIS[ler_inteiro("Tipo de imóvel: ", 1, 3)]
    quartos, vagas, tem_criancas = 0, 0, True
    if imovel.nome == "Estúdio":
        if ler_sim_nao("Deseja o pacote de duas vagas? [S/N]: "):
            vagas = 2 + ler_inteiro("Quantas vagas adicionais? ", 0)
    else:
        quartos = ler_inteiro("Quantidade de quartos [1 ou 2]: ", 1, 2)
        vagas = int(ler_sim_nao("Deseja uma vaga de garagem? [S/N]: "))
        if imovel.nome == "Apartamento":
            tem_criancas = ler_sim_nao("Possui crianças? [S/N]: ")
    parcelas = ler_inteiro("Parcelas da taxa contratual [1 a 5]: ", 1, 5)
    return Orcamento(imovel, quartos, vagas, tem_criancas, parcelas)


def mostrar_resumo(orcamento: Orcamento) -> None:
    print(f"\nOrçamento | {orcamento.imovel.nome}")
    if orcamento.quartos:
        print(f"Quartos: {orcamento.quartos}")
    print(f"Vagas: {orcamento.vagas}")
    for item, valor in orcamento.detalhar_aluguel().items():
        prefixo = "- " if item == "Desconto mensal" and valor else ""
        print(f"{item}: {prefixo}{brl(valor)}")

    print(f"\nTaxa contratual: {brl(orcamento.TAXA_CONTRATUAL)}")
    for numero, valor in enumerate(orcamento.parcelas_contrato(), start=1):
        print(f"Parcela {numero}/{orcamento.parcelas}: {brl(valor)}")


def exportar_csv(orcamento: Orcamento, destino: Path) -> None:
    with destino.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["Mês", "Aluguel mensal (R$)", "Parcela contratual (R$)", "Total do mês (R$)"])
        for mes, aluguel, taxa, total in orcamento.projetar():
            escritor.writerow([mes, valor_decimal(aluguel), valor_decimal(taxa), valor_decimal(total)])


def main() -> int:
    try:
        orcamento = coletar_orcamento()
    except (EOFError, KeyboardInterrupt):
        print("\nOrçamento cancelado.")
        return 1

    mostrar_resumo(orcamento)
    destino = Path("projecao_12_meses.csv")
    try:
        exportar_csv(orcamento, destino)
    except OSError as erro:
        print(f"Não foi possível gravar o CSV: {erro}")
        return 1

    print(f"\nCSV de 12 meses gerado em: {destino.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
