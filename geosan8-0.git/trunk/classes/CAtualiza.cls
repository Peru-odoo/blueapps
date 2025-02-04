VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "CAtualiza"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'Atualiza a aplica��o GeoSanIni.exe quando necess�rio

' Atualiza a aplica��o local do usu�rio depois que o diret�rio do servidor foi atualizado
'
' AtualizaAplicacaoLocal - retorna verdadeiro se atualizou com sucesso e falso se ocorreu algum problema na atualiza��o
'
Public Function AtualizaAplicacaoLocal() As Boolean
    On Error GoTo Trata_Erro:
    Dim versaoAtu As CGetVersion        'para obter a vers�o da aplica��o
    Dim mensagemAtu As Boolean
    Dim diretorioServLocal As String    'diret�rio local onde est�o todas as atualiza��es baixadas da web p.ex: c:\tempApp
    Dim versaoAplicacao As String       'n�mero da vers�o atual da aplica��o GeoSanIni.exe
    Dim versaoServidor As String        'n�mero da vers�o que foi atualizada e est� dispon�vel
    Dim retornoAtu As Boolean           'se a c�pia foi realizada com sucesso ou n�o
    
    Set versaoAtu = New CGetVersion
    diretorioServLocal = ReadINI("ATUALIZACAO", "DIRETORIOLOCAL", App.path & "\CONTROLES\GEOSAN.INI")
    If versaoAtu.ExisteArquivo(App.path & "\GeoSanIni.exe") Then
        versaoAplicacao = versaoAtu.ObtemVersao(App.path & "\GeoSanIni.exe")
    Else
        ErroUsuario.Registra "GeoSan.exe-CAtualiza", "AtualizaAplicacaoLocal", CStr(Err.Number), CStr(Err.Description), False, True, "N�o encontrou o arquivo: " & App.path & "\GeoSanIni.exe - A aplica��o continuou rodando normalmente."
        AtualizaAplicacaoLocal = False
        Exit Function
    End If
    If versaoAtu.ExisteArquivo(diretorioServLocal & "\GeoSanIni.exe") Then
        versaoServidor = versaoAtu.ObtemVersao(diretorioServLocal & "\GeoSanIni.exe")
    Else
        ErroUsuario.Registra "GeoSan.exe-CAtualiza", "AtualizaAplicacaoLocal", CStr(Err.Number), CStr(Err.Description), False, True, "N�o encontrou o arquivo: " & diretorioServLocal & "\GeoSanIni.exe - A aplica��o continuou rodando normalmente."
        AtualizaAplicacaoLocal = False
        Exit Function
    End If
    If versaoAplicacao <> versaoServidor Then
        FileCopy diretorioServLocal & "\GeoSanIni.exe", App.path & "\GeoSanIni.exe"
        ErroUsuario.Registra "GeoSan.exe-CAtualiza", "AtualizaAplicacaoLocal", CStr(Err.Number), CStr(Err.Description), False, True, "Copiou o arquivo " & diretorioServLocal & "\GeoSanIni.exe ---> " & App.path & "\GeoSanIni.exe - Atualizando o mesmo com sucesso."
    End If
    AtualizaAplicacaoLocal = True
    Exit Function
    
Trata_Erro:
    If Err.Number = 0 Or Err.Number = 20 Then
        Resume Next
    Else
       ErroUsuario.Registra "GeoSan.exe-CAtualiza", "AtualizaAplicacaoLocal", CStr(Err.Number), CStr(Err.Description), False, glo.enviaEmails
    End If
End Function
