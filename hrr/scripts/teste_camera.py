from ..hrr.visao import Visao, Teste

def main():
    vis = Visao(Teste())
    print(vis.decisao_alinhamento())
    vis.desenhar_bordas()
    vis.desenhar_alinhamento()
    vis.decisao_alinhamento()
main()