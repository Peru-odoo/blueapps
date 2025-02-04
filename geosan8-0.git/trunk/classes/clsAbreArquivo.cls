VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "clsAbreArquivo"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' Esta classe � respons�vel por opera��es de abertura de arquivos com aplica��es associadas as suas respectivas extens�es
Option Explicit

'Declara fun��o para iniciar uma aplica��o associada com uma extens�o de um documento sem saber o nome da aplica��o associada
Private Declare Function ShellExecute Lib "shell32.dll" Alias _
      "ShellExecuteA" (ByVal hwnd As Long, ByVal lpszOp As _
      String, ByVal lpszFile As String, ByVal lpszParams As String, _
      ByVal lpszDir As String, ByVal FsShowCmd As Long) As Long

Private Declare Function GetDesktopWindow Lib "user32" () As Long   'retorna um handle para o desktop

'Defini��o de constantes de erro para o a fun��o ShellExecute
Const SW_SHOWNORMAL = 1
Const SE_ERR_FNF = 2&
Const SE_ERR_PNF = 3&
Const SE_ERR_ACCESSDENIED = 5&
Const SE_ERR_OOM = 8&
Const SE_ERR_DLLNOTFOUND = 32&
Const SE_ERR_SHARE = 26&
Const SE_ERR_ASSOCINCOMPLETE = 27&
Const SE_ERR_DDETIMEOUT = 28&
Const SE_ERR_DDEFAIL = 29&
Const SE_ERR_DDEBUSY = 30&
Const SE_ERR_NOASSOC = 31&
Const ERROR_BAD_FORMAT = 11&

'Fun��o para abrir um arquivo com a aplica��o associada a extens�o do mesmo
'
' DocName - nome do arquivo a ser aberto
'
Private Function StartDoc(DocName As String) As Long
          On Error GoTo Trata_Erro:
          Dim Scr_hDC As Long
          Scr_hDC = GetDesktopWindow()
          StartDoc = ShellExecute(Scr_hDC, "Open", DocName, _
          "", "C:\", SW_SHOWNORMAL)
    Exit Function
    
Trata_Erro:
    If Err.Number = 0 Or Err.Number = 20 Then
        Resume Next
    Else
        ErroUsuario.Registra "clsAbreArquivo", "StartDoc", CStr(Err.Number), CStr(Err.Description), True, glo.enviaEmails
    End If
End Function
'Subrotina para abrir um arquivo com a aplica��o associada a extens�o do mesmo.
'Esta fun��o verifica se houve erro na abertura e mostra mensagem de erro que ocorreu
'
' nomeArquivo - nome do arquivo, podendo conter o n�mero do disco (c:\ por exemplo) a ser aberto pela aplica��o associada a extens�o do mesmo.
'
Public Sub Abre(nomeArquivo As String)
    On Error GoTo Trata_Erro:
    Dim r As Long, msg As String
    r = StartDoc(nomeArquivo)         'chama o arquivo a ser aberto
    If r <= 32 Then
        'There was an error
        Select Case r
            Case SE_ERR_FNF
                msg = "GeoSan: O arquivo n�o foi encontrado"
            Case SE_ERR_PNF
                msg = "GeoSan: O diret�rio n�o foi encontrado"
            Case SE_ERR_ACCESSDENIED
                msg = "GeoSan: Acesso negado"
            Case SE_ERR_OOM
                msg = "GeoSan: Disco cheio"
            Case SE_ERR_DLLNOTFOUND
                msg = "GeoSan: DLL n�o encontrada"
            Case SE_ERR_SHARE
                msg = "GeoSan: Ocorreu uma viola��o de compartilhamento"
            Case SE_ERR_ASSOCINCOMPLETE
                msg = "GeoSan: Associa��o de arquivo incompleta ou inv�lida"
            Case SE_ERR_DDETIMEOUT
                msg = "GeoSan: Tempo limite de DDE atingido"
            Case SE_ERR_DDEFAIL
                msg = "GeoSan: Transa��o de DDE falhou"
            Case SE_ERR_DDEBUSY
                msg = "GeoSan: DDE em uso/ocupada"
            Case SE_ERR_NOASSOC
                msg = "GeoSan: N�o existe associa��o para a extens�o do arquivo"
            Case ERROR_BAD_FORMAT
                msg = "GeoSan: Erro de arquivo execut�vel inv�lido ou erro na imagem do arquivo execut�vel"
            Case Else
                msg = "GeoSan: Erro desconhecido"
        End Select
        MsgBox msg
    End If
    Exit Sub
    
Trata_Erro:
    If Err.Number = 0 Or Err.Number = 20 Then
        Resume Next
    Else
        ErroUsuario.Registra "clsAbreArquivo", "Abre", CStr(Err.Number), CStr(Err.Description), True, glo.enviaEmails
    End If
End Sub

