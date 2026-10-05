from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request
from app.schemas.schemas_usuarios import CadastroUsuarioSchema, RespostaUsuarioSchema
from app.models.models_usuarios import Usuario
from app.database.session import get_db
from app.core.security import gerar_hash_senha

# cria o limitador de requisições

from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)

cadastro = APIRouter(tags=["Cadastro de Usuários"])

@cadastro.post("/cadastro-de-usuarios", response_model=RespostaUsuarioSchema)
@limiter.limit("5/minute", error_message="Limite de requisições excedido. Por favor, tente novamente mais tarde.")  # Limite de 5 requisições por minuto
async def criar_usuario(request: Request, usuario: CadastroUsuarioSchema, db=Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")

    usuario = Usuario(nome=usuario.nome, email=usuario.email, senha=gerar_hash_senha(usuario.senha))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return RespostaUsuarioSchema(nome=usuario.nome, email=usuario.email, message="Usuário cadastrado com sucesso.")
