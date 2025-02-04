VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "CPrintErro"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' Classe para informar o erro para o usu�rio e registrar o mesmo no arquivo de log
' Recebe os dados do erro, mostra mensagem ao usu�rio e registra no arquivo de log do sistema
'
' Modulo - string que cont�m em arquivo VB o erro ocorreu
' EVENTO - string que cont�m em que rotina o erro ocorreu
' ErrDescr - string com a descri��o do erro ocorrido
' ExibeMensagem - se � para exibir ou n�o uma mensagem para o usu�rio
' enviaEmail - verdadeiro ou falso, indicando se ir� enviar ou n�o um email para NEXUS com o erro que ocorreu
' linha - n�mero da linha ou descri��o da localiza��o em que o erro ocorreu
'
' Exemplo de uso desta classe: ErroUsuario CStr(Me.Name), "nome do evento que o mesmo ocorreu, atrav�s de mensagem digitada pelo programador", CStr(Err.Number), CStr(Err.Description), True, True
' C�digos de erros a serem tratados:
' 0  - The operation completed successfully
' 20 - The system cannot find the device specified
'
' Exemplo de c�digo para tratar o erro
'
'   Exit Function
'   Exit Sub
'Trata_Erro:
'    If Err.Number = 0 Or Err.Number = 20 Then
'        Resume Next
'    Else
'       ErroUsuario.Registra "CCoordIniFinLinha", "GetStartEndPointsTrecho", CStr(Err.Number), CStr(Err.Description), True, glo.enviaEmails
'    End If
'


Public Function Registra(ByVal Modulo As String, ByVal EVENTO As String, ByVal ErrNum As String, ByVal ErrDescr As String, ByVal ExibeMensagem As Boolean, ByVal enviaEmail As Boolean, Optional ByVal linha As String = "N�o registrada")
    On Error GoTo Trata_Erro:
    
    Dim nomeArquivoErro As String
    Dim sucesso As String
    
    nomeArquivoErro = Environ("HOMEDRIVE") & Environ("HOMEPATH")
    'nomeArquivoErro = Environ$("USERPROFILE") & "\Meus Documentos" & Environ("LOCALAPPDATA")
    nomeArquivoErro = nomeArquivoErro + "\GeoSanLogErro.txt"
    Close #1 'FECHA O ARQUIVO DE LOG
    Open nomeArquivoErro For Append As #1
    Print #1, "DATA"; Tab(20); Now
    Print #1, "Endere�o IP"; Tab(20); frmAtualiza.Winsock1.LocalIP
    Print #1, "Nome Computador"; Tab(20); frmAtualiza.Winsock1.LocalHostName
    Print #1, "ARQUIVO"; Tab(20); Modulo
    Print #1, "ROTINA"; Tab(20); EVENTO
    Print #1, "LINHA"; Tab(20); linha
    Print #1, ""
    Print #1, "C�DIGO ERRO"; Tab(20); ErrNum
    Print #1, "DESCRI��O"; Tab(20); ErrDescr
    Print #1, ""
    Print #1, "-----------------------------------------------------------------------------------------------------"
    Print #1, ""
    Close #1 'FECHA O ARQUIVO
    'SE O PAR�METRO ExibeMensagem = True , EXIBE MENSAGEM PARA O USU�RIO
    If enviaEmail = True Then
        sucesso = Email.enviaEmail(nomeArquivoErro)
        If sucesso <> "ok" Then
            MsgBox "Provavelmente voc� est� sem conex�o com a Internet, ou a mesma est� muito lenta. Favor verificar. Mensagem: " & sucesso & " Favor entrar em contato com o suporte t�cnico da NEXUS."
        End If
    End If
    If ExibeMensagem = True Then
        MsgBox "A opera��o n�o pode ser completada, favor enviar o arquivo: " & nomeArquivoErro & " para o suporte t�cnico da NEXUS para maiores detalhes.", vbInformation
    End If
    
Trata_Erro:
    If Err.Number = 0 Or Err.Number = 20 Then
        Resume Next
    Else
        MsgBox ("N�o exite permiss�o de acesso ao arquivo " + nomeArquivoErro)
        End
    End If
End Function
