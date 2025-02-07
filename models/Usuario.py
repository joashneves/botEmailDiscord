from models.db import _Sessao, Usuario, Seguindo, UsuariosBanidos

class Manipular_Servidor:
    def Obter_usuario(id_discord: int):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                print("usuario não existe")
                return "Usuario não existe"
            print(usuario)
            return usuario

    def Criar_usuario(id_discord: int, apelido:str, descricao:str, id_ServidorBase:int):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not usuario:
                NovoUsuario = Usuario(
                    id_discord=id_discord,
                    aceita_dm=True,
                    apelido=apelido,
                    descricao=descricao,
                    post=0,
                    id_ServidorBase=id_ServidorBase)
                sessao.add(NovoUsuario)
                print(f"Usuario criado {NovoUsuario}")
                return "Usuario criado"
            return "Usuario ja existe"
        
    def Atualiza_usuario(id_discord:int):
        with _Sessao() as sessao:
            usuario = sessao.query(Usuario).filter_by(id_discord=id_discord).first()
            if not Usuario:
                return "Usuario não registrado"
            usuario.post += 1;
            sessao.commit()
            return usuario
            