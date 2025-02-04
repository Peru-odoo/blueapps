VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "CArquivo"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
' Classe com opera��es em arquivos e diret�rios
Option Explicit

Private Const BIF_RETURNONLYFSDIRS = 1
Private Const BIF_DONTGOBELOWDOMAIN = 2
Private Const MAX_PATH = 260

Private Declare Function SHBrowseForFolder Lib "shell32" (lpbi As BrowseInfo) As Long

Private Declare Function SHGetPathFromIDList Lib "shell32" (ByVal pidList As Long, ByVal lpBuffer As String) As Long

Private Declare Function lstrcat Lib "kernel32" Alias "lstrcatA" (ByVal lpString1 As String, ByVal lpString2 As String) As Long

Private Type BrowseInfo
   hWndOwner As Long
   pIDLRoot As Long
   pszDisplayName As Long
   lpszTitle As Long
   ulFlags As Long
   lpfnCallback As Long
   lParam As Long
   iImage As Long
End Type

'Declara��es necess�rias para a fun��o GetMyDocumentsDirectory()
Const REG_SZ = 1
Const REG_BINARY = 3
Const HKEY_CURRENT_USER = &H80000001
Const SYNCHRONIZE = &H100000
Const STANDARD_RIGHTS_READ = &H20000
Const KEY_ENUMERATE_SUB_KEYS = &H8
Const KEY_NOTIFY = &H10
Const KEY_QUERY_VALUE = &H1
Const KEY_READ = ((STANDARD_RIGHTS_READ Or KEY_QUERY_VALUE Or KEY_ENUMERATE_SUB_KEYS Or KEY_NOTIFY) And (Not SYNCHRONIZE))

Private Declare Function RegOpenKeyEx Lib "advapi32.dll" Alias "RegOpenKeyExA" (ByVal hKey As Long, _
    ByVal lpSubKey As String, ByVal Reserved As Long, ByVal samDesired As Long, phkResult As Long) As Long
Private Declare Function RegQueryValueEx Lib "advapi32.dll" Alias "RegQueryValueExA" (ByVal hKey As Long, _
    ByVal lpValueName As String, ByVal lpReserved As Long, lpType As Long, lpData As Any, lpcbData As Long) As Long
Private Declare Function RegCloseKey Lib "advapi32.dll" (ByVal hKey As Long) As Long
' Sugest�o de rotina para o usu�rio selecionar um arquivo em que ser�o salvas informa��es
'    Dim selecionaArquivo As New CArquivo                                                    'para obter o nome e diret�rio onde o arquivo ser� salvo
'    Dim nomeArquivo As String                                                               'nome completo do arquivo com o drive e diret�rio no qual ser� salvo
'    Dim diretorioMyDocuments As String                                                      'diret�rio meus documentos inicial
'    Dim filelocation As String                                                              'nome completo do arquivo onde ser� salvo o relat�rio
'
'    nomeArquivo = selecionaArquivo.ConfiguraNomeArquivo("exporta��o_dados_redes", "txt", diretorioMyDocuments)  'obtem o nome do arquivo sugerido e o diret�rio meus documentos do usu�rio
'    CommonDialog1.Filter = "Texto (.txt)|*.TXT|Todos tipos (*.*)|*.*|"                                          'configura o filtro do arquivo
'    CommonDialog1.filename = nomeArquivo                                                                        'informa a caixa de di�logo que ser� aberta o nome do arquivo inicial sugerido
'    CommonDialog1.InitDir = diretorioMyDocuments                                                                'sugero o diret�rio inicial
'    CommonDialog1.ShowSave                                                                                      'abre a caixa de di�logo par ao usu�rio digitar o nome do arquivo e selecionar o diret�rio, se desejar
'    filelocation = CommonDialog1.filename

' Fun��o para definir previamente um nome de arquivo
'
' Retorna um diret�rio junto com o nome do arquivo
' nomeArquivo - nome do arquivo que ser� concatenado junto ao restante das informa��es
' extensao - extensao do arquivo sem o ponto
' diretoiro - em que o arquivo ser� salvo. Retorna este valor
'
Public Function ConfiguraNomeArquivo(nomeArquivo As String, extensao As String, ByRef diretorio As String) As String
    diretorio = GetMyDocumentsDirectory()
    ConfiguraNomeArquivo = Format(Now, "YYYY-MM-DD-HHMMSS") & "-" & nomeArquivo & "." & extensao
End Function


' Fun��o para a sele��o de um diret�rio por parte do usu�rio
'
' Retorna a string contendo o nome do diret�rio completo
'
Public Function SelecionaDiretorio() As String
    Dim lpIDList As Long ' Declare Varibles
    Dim sBuffer As String
    Dim szTitle As String
    Dim tBrowseInfo As BrowseInfo
    
    szTitle = "Selecione o diret�rio onde ser�o exportados os arquivos"
    ' Text to appear in the the gray area under the title bar
    ' telling you what to do
    
    With tBrowseInfo
        .hWndOwner = FrmMain.hwnd ' Owner Form
        .lpszTitle = lstrcat(szTitle, "")
        .ulFlags = BIF_RETURNONLYFSDIRS + BIF_DONTGOBELOWDOMAIN
    End With
    
    lpIDList = SHBrowseForFolder(tBrowseInfo)
    
    If (lpIDList) Then
        sBuffer = Space(MAX_PATH)
        SHGetPathFromIDList lpIDList, sBuffer
        sBuffer = Left(sBuffer, InStr(sBuffer, vbNullChar) - 1)
    Else
        sBuffer = "falhou"
    End If

    SelecionaDiretorio = sBuffer
End Function
' Fun��o para retornar o prefixo com a data e hora em que os arquivos foram gerados
'
' Retorna a data seguida da hora para ser incorporada no arquivo de exporta��o
'
Public Function prefixo() As String
    Dim dataHora As String
    
    dataHora = DateValue(Now) & " " & TimeValue(Now)               'define o nome completo do prefixo do arquivo, inclu�ndo a data e hora em que o mesmo ser� gerado pela primeira vez
    dataHora = Replace(dataHora, "/", "-")                        'troca caractere / especial que n�o � aceito como parte do nome do arquivo
    dataHora = Replace(dataHora, ":", "-")                        'troca caractere : especial que n�o � aceito como parte do nome do arquivo
    dataHora = dataHora + " - "
    prefixo = dataHora
End Function
'Obtem o nome do diret�rio dos Meus Documentos do usu�rio que est� logado
'
'GetMyDocumentsDirectory() - retorna o caminho do diret�rio
'
Private Function GetMyDocumentsDirectory() As String
    Dim lRes As Long
    Dim lResult As Long, lValueType As Long, strBuf As String, lDataBufSize As Long
    Dim strData As Integer
    RegOpenKeyEx HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders", 0, KEY_READ, lRes
    lResult = RegQueryValueEx(lRes, "Personal", 0, lValueType, ByVal 0, lDataBufSize)
    If lResult = 0 Then
        If lValueType = REG_SZ Then
            strBuf = String(lDataBufSize, Chr$(0))
            lResult = RegQueryValueEx(lRes, "Personal", 0, 0, ByVal strBuf, lDataBufSize)
            If lResult = 0 Then
                GetMyDocumentsDirectory = Left$(strBuf, InStr(1, strBuf, Chr$(0)) - 1)
            End If
        End If
    End If
    RegCloseKey lRes
End Function
