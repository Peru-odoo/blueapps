VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "CDownload"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' Classe para realizar download de arquivos

Private b() As Byte                             'contem o arquivo em que ser� realizado o download
Private nomeUrl As String                       'caminho em que est� o arquivo em que ser� realizado o download
Private proxyNome As String                     'nome do servidor Proxy da empresa, caso exista
Private proxyUsuario As String                  'login do usu�rio para acessar o Proxy interno da empresa, caso exista
Private proxySenha As String                    'senha do usu�rio para acessar o Proxy interno da empresa, caso exista
Private proxyPort As String                     'n�mero da porta do servidor Proxy interno da empresa
Private diretorioComputador As String                'nome do diret�rio local onde ser� realizado o download da atualiza��o
Private nomeArquivoAtualizacoes As String       'nome do arquivo remoto que contem as atualiza��es a serem realizadas
Private diretorioRemoto As String               'nome do diret�rio remoto onde est�o todas as atualiza��es
Private web As String                           'se a atualiza��o vem da WEB ou de um diret�rio. Se vir da Web � SIM, caso contr�rio NAO
Private portaWeb As String                      'n�mero da porta web em que est� o servidor de arquivos

Property Let url(nomeU As String)               'recebe o caminho em que est� o arquivo em que ser� realizado o download
    nomeUrl = nomeU
End Property

Property Let proxy(proxyN As String)            'recebe o nome da porta do proxy
    proxyNome = proxyN
End Property

Property Let proxyUser(proxyU As String)        'recebe o nome do usu�rio que acessa o proxy
    proxyUsuario = proxyU
End Property

Property Let proxyPass(proxyP As String)        'recebe a senha do usu�rio que acessa o proxy
    proxySenha = proxyP
End Property

Property Let proxyPorta(proxyP As String)       'recebe o n�mero da porta do proxy
    proxyPort = proxyP
End Property
Property Let diretorioLocal(diretorioL As String)   'nome do diret�rio local onde ser�o baixadas todas as atualiza��es
    diretorioComputador = diretorioL
End Property
Property Get diretorioLocal() As String         'retorna o valor do diret�rio local
    diretorioLocal = diretorioComputador
End Property


Property Let diretorioServidor(diretorioS As String) 'nome do diret�rio remoto onde est�o todas as atualiza��es
    diretorioRemoto = diretorioS
End Property

Property Let atualizacaoWeb(atWeb As String)         'pode ser SIM ou NAO, inidica se a atualiza��o vem da Web (SIM) ou de um diret�rio (NAO)
    web = atWeb
End Property

Property Let portaWww(ptW As String)
    portaWeb = ptW
End Property
Public Function DownloadArquivo(arquivoDownload As String) As Boolean
    On Error GoTo Trata_Erro:
    Dim url As String
    Dim nomeDownloadLocal As String
    
    Set ErroUsuario = New CPrintErro
    nomeDownloadLocal = diretorioComputador & "\" & arquivoDownload
    If web = "NAO" Then                                                     'est� copiando a partir de um diret�rio local
        url = nomeUrl & diretorioRemoto & "\" & arquivoDownload
        FileCopy url, nomeDownloadLocal
    Else                                                                    'est� copiando a partir do site da NEXUS
        If proxyNome <> "NULO" Then                                         'existe um servidor Proxy
            frmAtualiza.Inet1.AccessType = icNamedProxy                     'para indicar que o acesso a internet ser� via um servidor proxy nomeado
            frmAtualiza.Inet1.proxy = proxyNome & ":" & proxyPort
            frmAtualiza.Inet1.UserName = proxyUsuario
            frmAtualiza.Inet1.Password = proxySenha
        End If
        url = nomeUrl & ":" & portaWeb & diretorioRemoto & "/" & arquivoDownload
        frmAtualiza.Inet1.url = url
        b() = frmAtualiza.Inet1.OpenURL(url, icByteArray)
        Open nomeDownloadLocal For Binary Access Write As #1
        Put #1, , b()
        Close #1
   End If
    DownloadArquivo = True
    Exit Function
    
Trata_Erro:
    If Err.Number = 0 Or Err.Number = 20 Then
        Resume Next
    Else
        ErroUsuario.Registra "CDownload", "DownloadArquivo: " & arquivoDownload, CStr(Err.Number), CStr(Err.Description), False, True
        DownloadArquivo = False
    End If
End Function

Public Function VerificaAtualizacoes() As Boolean

End Function

