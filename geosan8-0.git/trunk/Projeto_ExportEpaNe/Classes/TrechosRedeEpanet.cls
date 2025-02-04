VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "TrechosRedeEpanet"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'Esta classe � referente ao processamento dos trechos de redes que foram selecionados para exporta��o para o EPANET
'
'
Option Explicit
Private conBd As ADODB.Connection
Private trechos As New TrechosRedeEpanet
Private usuario_global As String
Private conn_global As ADODB.Connection
Private az As Integer
Private rsWaterCompTypes As New ADODB.Recordset         'RecordSet de referencia para consulta do tipo de componente
Private blnRsWaterCompTypes As Boolean                  'Indicador para informar se a tabela RsWaterCompTypes foi carregada com registros
Private strTipoComp As String                           'Vari�vel que receber� o tipo de componente (Junction, valve,pump...)
Private rsNos As ADODB.Recordset                        'Cursor Tempor�rio que retonar� todos os nos da Rede para abastecer o RsNosTMP
Private rsNos2 As Recordset
Private tb As New TeDatabase

'Realiza toda a exporta��o para o EPANET
'
'
'Procedimento Exporte EPANET recebe como parametros o cursor trazendo todas os trechos
'a serem exportados e o objecto de conex�o
'(rsTrechos):� a tabela Waterlines com os filtros de tipo de rede e setor selecionados pelo usu�rio (TIPO=1 na tabela POLIGONO_SELECAO)
'arquivoLog: nome do arquivo onde est� sendo escrito todo o log do sistema
'
'
Function Exporta()
    Dim tipoErro As String                              'indica para o arquivo de log o tipo de erro que pode estar acontecendo
    
    tipoErro = "Erro n�o localizado"
    'Neste arquivo existe gravado o nome do usu�rio ativo, que indica que usu�rio exportou para o Epanet o pol�gono de sele��o
    'Atrav�s dele ser� feita uma pesquisa no banco de dados POLIGONO_SELECAO para ver que redes OBJECT_ID_s ser�o exportados para o EPANET
    'Lembrando que
    '                TIPO = 0 - N�s
    '                TIPO = 1 - Redes
    '                TIPO = 2 - Ramais

    banco.AtualizaAsRugosidades                         'realiza a atualiza��o, no banco geogr�fico do GeoSan, de todas as rugosidades a partir do material de cada rede de �gua
    banco.ZeraMateriais                                 'Zera todos os materiais de tubula��es quando o mesmo n�o estiver cadastrado
    banco.AbrirEstruturaExporteRede
    usuario_global = trechos.ObtemUsuario
    ExportaParaEpanet                                   'inicia a exporta��o para o EPANET
    banco.GeraArquivo_de_Saida                          'Gera o arquivo .INP de sa�da para o Epanet
    Screen.MousePointer = vbNormal
End Function

'Obtem o nome do usu�rio que est� exportando para o EPANET
'
'
Function ObtemUsuario() As String
    Dim retval As String
    Dim usuario As String

    retval = Dir(App.Path & "\Controles\UserLog.txt")
    If retval <> "" Then                                                'verifica se o arquivo existe na pasta
        Open App.Path & "\Controles\UserLog.txt" For Input As #3        'Abre e l� o arquivo para ver que usu�rio ser� consultado no pol�gono selecionado, pois podem existir v�rios usu�rios realizando esta opera��o ao mesmo tempo
        Line Input #3, usuario
        Close #3
    Else
        MsgBox "� necess�rio criar a sele��o por pol�gono.", vbOKOnly + vbInformation, "Mensagem"  'Avisa e cai fora, pois n�o d� para executar a opera��o
        End
    End If
    usuario_global = usuario
    ObtemUsuario = usuario
End Function

'Exporta para o EPANET
'
'
Function ExportaParaEpanet()
    Dim no As String                                                    'Vaviavel que guadar� o n� a ser processado
    Dim contadorTrechos As Integer                                      'para contar quantos trechos est� exportando
    Dim mPROVEDOR As String
    Dim mSERVIDOR As String
    Dim mPORTA As String
    Dim mBANCO As String
    Dim mUSUARIO As String
    Dim Senha As String
    Dim decriptada As String
    Dim prov As String
    Dim numeroErro As String                                            'para auxiliar a identificar onde ocorreu o erro
    Dim conta_no As Integer                                             'Vari�vel contador para repeti��o do processo para o no inicial e final de cada trecho
    Dim Lin_len As Double, x As Double, y As Double                     'Vari�veis que retornar�o a posi��o do ponto virtual
    Dim NoI As String, NoF As String                                    'Vari�veis que guardar�o os n�s para inser��o do trecho
    Dim retorno As Double, distancia As Double, novoLinLen As Double
    Dim numTotalVerticesNaLinha As Integer
    Dim i As Integer
    Dim teNet As New TECOMNETWORKLib.TeNetwork
    Dim geom_id As Long, rightside As Long, adjust As Long               'Vari�veis da biblioteca
    Dim Object_id As String
    Dim xpinter As Double, ypinter As Double, metricValue As Double
    Dim verticeInicial_x As Double, verticeInicial_y As Double, vertice_Y As Double, vertice_X As Double
    Dim idLinha As String
    Dim idNo As String
    
    Open "C:\Program Files\GeoSan\Controles\testeExportacaoEpanet.txt" For Append As #20
    Print #20, "In�cio"
    Close #20
    
    contadorTrechos = 0                                                                                 'Informa que o contador de trechos exportados � zero
    If (az <> 10) Then
        mSERVIDOR = ReadINI("CONEXAO", "SERVIDOR", App.Path & "\CONTROLES\GEOSAN.ini")
        mPORTA = ReadINI("CONEXAO", "PORTA", App.Path & "\CONTROLES\GEOSAN.ini")
        mBANCO = ReadINI("CONEXAO", "BANCO", App.Path & "\CONTROLES\GEOSAN.ini")
        mUSUARIO = ReadINI("CONEXAO", "USUARIO", App.Path & "\CONTROLES\GEOSAN.ini")
        Senha = ReadINI("CONEXAO", "SENHA", App.Path & "\CONTROLES\GEOSAN.ini")
        prov = ReadINI("CONEXAO", "PROVEDOR", App.Path & "\CONTROLES\GEOSAN.ini")
        decriptada = FunDecripta(Senha)
        az = 10
    End If
    tb.Provider = Provider                                                                              'Configura o objeto tb(Tecomdatabase) que ser� usado para retornar para as vari�veis lin_len, x e y seus valores para cada trecho
    tb.Connection = conn
    tb.setCurrentLayer "WATERLINES"
    teNet.Provider = 1
    teNet.Connection = conn                                                                             'configura o componente para conexao com o banco de dados
    teNet.setCurrentLayer "WATERLINES"                                                                  'seta o plano "WATERLINES" como corrente
    trechos.AbrirEstruturaExporteRede                                                                   'Abre os cursores que guardar�o os objectos do rede(nos,trechos,etc) em memoria para serem gerados em arquivo txt
    banco.RsWaterCompTypes_Inicializa                                                                   'para ver quais os tipos de par�metros para redes, bombas, v�lvulas, etc. e cria um vetor com todos eles
    banco.CarregaRsNosTMP                                                                               'Carrega RsNosTMP em memoria, tranferes os dados do cursor no servidor para a maquina rsNosTmp = rsNos
        
    Do While Not banco.Rs_trechosDeRede_terminouDeLer = True                                            'Percorre todos os trechos da tabela waterlines com a clausura where (setor e tipo de rede), com o pol�gono de sele��o, ativada e cursor iniciando no primeiro registro
        DoEvents
        If Cancelar = True Then
           Return
        End If
        contadorTrechos = contadorTrechos + 1                                                           'Incrementa o contador de trechos lidos
        For conta_no = 1 To 2                                                                           'para cada um dos n�s do trecho d rede, atribui o ID do n� ao n� inicial ou final. Percorre os dois n�s do Trecho
            If conta_no = 1 Then                                                                        'se estamos com o n� inicial do trecho, primeira passagem do FOR
                no = banco.rs_trechosDeRede_numeroNoInicial
            Else                                                                                        'se estamos com o n� final do trecho, segunda passagem do FOR
                no = banco.rs_trechosDeRede_numeroNoFinal
            End If
            If Not banco.RsTrechosExportados_verificaSeFoiExportado(banco.rs_trechosDeRede_ObjectIdDoTrecho) Then           'verifica se o trecho (selecionado pela cerca do GeoSan) n�o foi exportado, se n�o foi exportado, vamos processar
                idLinha = banco.rs_trechosDeRede_ObjectIdDoTrecho                                       'obtem o OBJECT_ID do trecho de rede (selecionado pela cerca) que estamos exportando para o EPANET
                idNo = no
                If conta_no = 1 Then                                                                    '� o n� inicial do trecho de rede (primeira passagem), atribui ao n� inicial
                   NoI = no
                Else                                                                                    '� o n� final do trecho de rede (primeira passagem), atribui ao n� final
                   NoF = no
                End If
                If banco.RsNosExportados_esteNoJaFoiExportado(no) = False Then                          'se o n� n�o foi exportado ainda
                    Open "C:\Program Files\GeoSan\Controles\testeExportacaoEpanet.txt" For Append As #20
                    Print #20, "No exportado: " + no
                    Close #20
                    banco.RsNosTmp_filtraPorNo (no)                                                     'filtra para pegar os dados somente do n� que est� sendo lido
                    strTipoComp = banco.RsWaterCompTypes_tipoDeEspecificacao                            'Obter a especifica��o para poder processar a exporta��o conforme o tipo de n�
                    Open "C:\Program Files\GeoSan\Controles\testeExportacaoEpanet.txt" For Append As #20
                    Print #20, "Tipo de componente recebido: " + strTipoComp + " para o n�: " + no
                    Close #20
                    If banco.RsWaterCompTypes_ExitemParametros = True Then
                        Select Case strTipoComp                                 'Seleciona do processo a ser usado para o tipo do n�
                            'Case No_Bombas, No_Valvulas, No_Valvulas_99 'Especial n�
                            '� uma verifica��o realizada na coluna Specification_ da tabela WaterComponentsTypes
                            'Mudando nesta tabela o valor de Specification_ muda se o n� ser� exportado como v�lvula (pequeno trecho) ou n�o
                            Case "PUMP", "VALVE", "VALVE2", "REGISTER"                                  'vai dividir uma v�lvula, registro, etc, que � representado por um n�, em dois n�s e um trecho
                                Call ConverteNoEmTrecho(idLinha, Lin_len, conta_no, numTotalVerticesNaLinha, distancia, no, NoI, NoF)
                            Select Case strTipoComp
                                Case "PUMP"
                                    Call banco.RsPumps_adicionaBomba(no, conta_no)                      'adiciona os dados da bomba para poder exportar depois para o EPANET
                                Case "VALVE"
                                    Call banco.RsValves_adicionaValvula(no)                             'adiciona os dados da v�lvula para poder exportar depois para o EPANET
                                Case "VALVE2"
                                    Call banco.RsValves2_adicionaValvula(no)                            'adiciona os dados da v�lvula2 para poder exportar depois para o EPANET
                                Case "REGISTER"
                                    Call banco.RsPipes_adicionaRegistro(no)                             'adiciona os dados do registro, na verdade um registro � um trecho de rede, para poder depois exportar para o EPANET
                            End Select
                        End Select
                    End If
                    Select Case strTipoComp                                                             'Insere o n� processado
                        Case "RNV"
                            Call banco.RsTanks_adicionaReservatorioNivelVariavel(no)                    'Adiciona os dados do RNV (Reservat�rio de N�vel Vari�vel) para poder exportar para o EPANET
                        Case "RNF"
                            Call banco.RsReservois_adicionaReservatorioNivelFixo(no)                    'Adiciona os dados do RNF (Reservat�rio de N�vel Fixo) para poder exportar para o EPANET
                        Case Else
                            Call banco.RsJunctions_adicionaJuncao(no, banco.RsNosTmp_obtemDemandaDoNo)  'Adiciona os dados da jun��o para poder exportar depois para o EPANET
                    End Select
                    Call banco.RsCoordinates_adicionaCoordenadas(no, banco.RsNosTmp_coordX(no), banco.RsNosTmp_coordY(no))  'Adiciona as coordenadas geogr�ficas de um n�, para o mesmo poder exportar para o EPANET
                End If
                banco.RsNosExportados_insereNoExportado (no)                                            'Insere o NO no cursor tempor�rio rsNosExportados
            End If
        Next
        
        Call banco.RsPipes_adicionaTrechoRede(idLinha, NoI, NoF)                                        'Insere o trecho no cursor tempor�rio rsPipes
        numTotalVerticesNaLinha = tb.getQuantityPointsLine(0, idLinha)                                  'obtem o n�mero de v�rtices existentes no trecho de rede que foi inserido
        If numTotalVerticesNaLinha > 2 Then                                                             'existem v�rtice intermedi�rios na linha que necessitam ser considerados no Epanet, pois 2 j� existem, o in�cial e final
            For i = 1 To numTotalVerticesNaLinha - 2                                                    'percorra do primeiro ao �ltimo v�rtice do trecho de rede
                If tb.getPointOfLine(0, idLinha, i, vertice_X, vertice_Y) Then                          'obtem as coordenadas do v�rtice
                    Call banco.RsVertices_adicionaVerticesDosTrechosRede(idLinha, vertice_X, vertice_Y) 'insere o v�rtice
                End If
            Next
        End If
        banco.RsTrechos_adicionaIdDoTrecho                                                              'Adiciona o Id do trecho de rede que j� foi exportado para o vetor de trechos exportados
        If FrmEPANET.ProgressBar1.Value < FrmEPANET.ProgressBar1.Max Then                               'Atualiza o formulario frmOdometro, para que o usu�rio saiba que o processamento est� andando
            FrmEPANET.ProgressBar1.Value = FrmEPANET.ProgressBar1.Value + 1
        End If
        banco.Rs_trechosDeRede_moveParaProximo
    Loop
End Function

'Converte um ponto (n�) em trecho.
'Isto � realizado quando tempos bomba, v�lvulas ou registros, pois no EPANET estes elementos s�o trechos de rede e n�o n�s
'Verifica a Dire��o da Tubula��o e recupera um ponto X_NO_VIRT, Y_NO_VIRT a 1/3 da distancia
'e insere o no virtual em RsJuntions e RsCoordinates
'
Private Function ConverteNoEmTrecho(idLinha As String, Lin_len As Double, conta_no As Integer, numTotalVerticesNaLinha_ As Integer, distancia As Double, no As String, NoI As String, NoF As String)
    Dim retorno As Double
    Dim X_Componente As Double                                                                  'COORDENADA X DO VERTICE
    Dim Y_Componente As Double                                                                  'COORDENADA Y DO VERTICE
    Dim X_Vertice As Double                                                                     'COORDENADA X DO VERTICE
    Dim Y_Vertice As Double                                                                     'COORDENADA Y DO VERTICE
    Dim VERTICE_LEN As Double                                                                   'ARMAZENA O COMPRIMENTO DO VERTICE ANALIZADO
    Dim X_NO_VIRT As Double                                                                     'ARMAZENA A COORDENADA X DO N� VIRTUAL CASO SEJA NECESS�RIO
    Dim Y_NO_VIRT As Double                                                                     'ARMAZENA A COORDENADA Y DO N� VIRTUAL CASO SEJA NECESS�RIO
    
    tb.getLengthOfLine 0, idLinha, Lin_len                                                      'carrega em Lin_len o comprimento total da linha
    
    If conta_no = 2 Then                                                                        'se for o ponto final pega a dist�ncia de 2/3 do comprimento da linha
        numTotalVerticesNaLinha_ = tb.getQuantityPointsLine(0, idLinha)                         'retorna n�mero de pontos que comp�em a linha. se maior que 2 significa que tem vertices
        If numTotalVerticesNaLinha_ > 2 Then 'existem v�rtices na linha
            retorno = tb.getPointOfLine(0, idLinha, (numTotalVerticesNaLinha_ - 2), X_Vertice, Y_Vertice)       'Pegar o penultimo ponto(vertice) RETORNA A COORDENADA DO �LTIMO VERTICE
            retorno = tb.getPointOfLine(0, idLinha, (numTotalVerticesNaLinha_ - 1), X_Componente, Y_Componente) 'RETORNA A COORDENADA DO �LTIMO N�
            VERTICE_LEN = DistanceBetween(X_Vertice, Y_Vertice, X_Componente, Y_Componente)     'RETORNA A DISTANCIA ENTRE O ULTIMO N� E O ULTIMO VERTICE
            distancia = (Lin_len - VERTICE_LEN) + (VERTICE_LEN * 0.666666)                      'DISTANCIA = COMPRIMENTO TOTAL DA LINHA - COMPRIMENTO DO ULTIMO VERTICE + 2 TER�OS DA DISTANCIA DO ULTIMO VERTICE
            tb.getPerpendicularPoint 0, idLinha, distancia, 0, X_NO_VIRT, Y_NO_VIRT             'CARREGA EM X_NO_VIRT E Y_NO_VIRT AS COORDENADAS DE LOCALIZA��O DO PONTO VIRTUAL QUE DEVER� SER CRIADO
        Else
            distancia = Lin_len * 0.666666                                                      'DISTANCIA = 2 TER�OS DO COMPRIMENTO TOTAL DA LINHA
            tb.getPerpendicularPoint 0, idLinha, distancia, 0, X_NO_VIRT, Y_NO_VIRT             'CARREGA EM X_NO_VIRT E Y_NO_VIRT AS COORDENADAS DE LOCALIZA��O DO PONTO VIRTUAL QUE DEVER� SER CRIADO
        End If
    Else                                                                                        ' se o ponto for o inicial, pega a dist�ncia de 1/3 do comprimento da linha
        numTotalVerticesNaLinha_ = tb.getQuantityPointsLine(0, idLinha)
        If numTotalVerticesNaLinha_ > 2 Then                                                    'existem v�rtices na linha
            retorno = tb.getPointOfLine(0, idLinha, 1, X_Vertice, Y_Vertice)                    'RETORNA A COORDENADA DO PRIMEIRO VERTICE
            retorno = tb.getPointOfLine(0, idLinha, 0, X_Componente, Y_Componente)              'RETORNA A COORDENADA DO PRIMEIRO N�
            VERTICE_LEN = DistanceBetween(X_Vertice, Y_Vertice, X_Componente, Y_Componente)     'RETORNA EM VERTICE_LEN A DISTANCIA ENTRE O PRIMEIRO VERTICE E O PRIMEIRO N�
            distancia = VERTICE_LEN * 0.33333                                                   'DISTANCIA = COMPRIMENTO TOTAL DA LINHA - COMPRIMENTO DO ULTIMO VERTICE + 2 TER�OS DA DISTANCIA DO ULTIMO VERTICE
            tb.getPerpendicularPoint 0, idLinha, distancia, 0, X_NO_VIRT, Y_NO_VIRT             'CARREGA EM X_NO_VIRT E Y_NO_VIRT AS COORDENADAS DE LOCALIZA��O DO PONTO VIRTUAL QUE DEVER� SER CRIADO
        Else
            distancia = Lin_len * 0.333333                                                      'DISTANCIA = 1 TER�O DO COMPRIMENTO TOTAL DA LINHA
            tb.getPerpendicularPoint 0, idLinha, distancia, 0, X_NO_VIRT, Y_NO_VIRT             'CARREGA EM X_NO_VIRT E Y_NO_VIRT AS COORDENADAS DE LOCALIZA��O DO PONTO VIRTUAL QUE DEVER� SER CRIADO
        End If
    End If
    Call banco.RsJunctions_adicionaJuncao(no & "A", 0#)                                         'adiciona o n� ao vetor de jun��es para depois poder export�-lo para o EPANET - coloca a demanda como zero, pois � um n� convertido em trecho por ser v�lvula, bomba ou registro
    Call banco.RsCoordinates_adicionaCoordenadas(no & "A", X_NO_VIRT, Y_NO_VIRT)                'Adiciona as coordenadas geogr�ficas de um n�, para o mesmo poder exportar para o EPANET - soma a letra A ao numero do n�, pois converteu o mesmo em dois, para representar um trecho, como o EPANET exige
    If conta_no = 1 Then                                                                        'Altera a vari�vel NoI ou NoF com o valor NO & "A" para ser usado na inser��o do trecho indicando que o trecho a ser inserido usar� um n� virtual
       NoI = no & "A"
    Else
       NoF = no & "A"
    End If
End Function

'Define a estrutura dos vetores que conter�o os dados que ser�o exportados para o Epanet
'
'
Sub AbrirEstruturaExporteRede()
    'coordenadas dos n�s
    rsCoordinates.Fields.Append "id", adVarChar, 255            'n�mero do n�
    rsCoordinates.Fields.Append "x", adDouble                   'coordenada X
    rsCoordinates.Fields.Append "y", adDouble                   'coordenada Y
    rsCoordinates.Open
    
    'tubula��es
    rsPipes.Fields.Append "id", adVarChar, 255                  'n�mero da tubula��o
    rsPipes.Fields.Append "node1", adVarChar, 255
    rsPipes.Fields.Append "node2", adVarChar, 255
    rsPipes.Fields.Append "length", adVarChar, 255
    rsPipes.Fields.Append "diameter", adDouble, 255
    rsPipes.Fields.Append "roughness", adDouble, 255
    rsPipes.Fields.Append "minorloss", adVarChar, 255
    rsPipes.Fields.Append "status", adVarChar, 255
    rsPipes.Fields.Append "Description", adVarChar, 255         'incluido em 13/05/2009 Jonathas
    rsPipes.Open
    
    'jun��es
    rsJunctions.Fields.Append "id", adVarChar, 255
    rsJunctions.Fields.Append "elev", adVarChar, 255
    rsJunctions.Fields.Append "demand", adDouble, 255
    rsJunctions.Fields.Append "pattern", adVarChar, 255
    rsJunctions.Open
    
    'bombas
    rsPumps.Fields.Append "id", adVarChar, 255
    rsPumps.Fields.Append "node1", adVarChar, 255
    rsPumps.Fields.Append "node2", adVarChar, 255
    rsPumps.Fields.Append "parameters", adVarChar, 255
    rsPumps.Fields.Append "potencia", adVarChar, 255
    rsPumps.Open
    
    'v�lvulas
    rsValves.Fields.Append "id", adVarChar, 255
    rsValves.Fields.Append "node1", adVarChar, 255
    rsValves.Fields.Append "node2", adVarChar, 255
    rsValves.Fields.Append "diameter", adVarChar, 255
    rsValves.Fields.Append "type", adVarChar, 255
    rsValves.Fields.Append "setting", adVarChar, 255
    rsValves.Fields.Append "minorloss", adVarChar, 255
    rsValves.Open
    
    'reservat�rios
    rsReservoirs.Fields.Append "ID", adVarChar, 255
    rsReservoirs.Fields.Append "Head", adVarChar, 255
    rsReservoirs.Fields.Append "Pattern", adVarChar, 255
    rsReservoirs.Open
    
    'tanques
    rsTanks.Fields.Append "ID", adVarChar, 255
    rsTanks.Fields.Append "Elevation", adVarChar, 255
    rsTanks.Fields.Append "InitLevel", adVarChar, 255
    rsTanks.Fields.Append "MinLevel", adVarChar, 255
    rsTanks.Fields.Append "MaxLevel", adVarChar, 255
    rsTanks.Fields.Append "Diameter", adVarChar, 255
    rsTanks.Fields.Append "MinVol", adVarChar, 255
    rsTanks.Fields.Append "VolCurve", adVarChar, 255
    rsTanks.Open
    
    'v�rtices de linhas de tubula��es
    rsVertices.Fields.Append "ID", adVarChar, 255               'n�mero da tubula��o
    rsVertices.Fields.Append "X-Coord", adDouble
    rsVertices.Fields.Append "Y-Coord", adDouble
    rsVertices.Open
    
    'n�s
    rsNosTmp.Fields.Append "ID", adVarChar, 255
    rsNosTmp.Fields.Append "X", adDouble
    rsNosTmp.Fields.Append "Y", adDouble
    rsNosTmp.Fields.Append "Tipo", adInteger
    rsNosTmp.Fields.Append "Padrao", adInteger
    rsNosTmp.Fields.Append "Curva", adInteger
    rsNosTmp.Fields.Append "Diametro", adVarChar, 255
    rsNosTmp.Fields.Append "Cota", adDouble
    rsNosTmp.Fields.Append "NivelMin", adDouble
    rsNosTmp.Fields.Append "NivelMax", adDouble
    rsNosTmp.Fields.Append "VolumeMin", adDouble
    rsNosTmp.Fields.Append "CurvaVol", adDouble
    rsNosTmp.Fields.Append "Parametros", adDouble
    rsNosTmp.Fields.Append "setting", adDouble
    rsNosTmp.Fields.Append "SubTypeValve", adDouble
    rsNosTmp.Fields.Append "demanda", adDouble
    rsNosTmp.Fields.Append "estado", adVarChar, 255
    rsNosTmp.Fields.Append "Description", adVarChar, 255
    rsNosTmp.Open
    
    'lista de trechos exportados
    rsTrechosExportados.Fields.Append "id", adVarChar, 255
    rsTrechosExportados.Open
    
    rsTrechos.Fields.Append "id", adVarChar, 255
    rsTrechos.Open
    
    'lista de n�s exportados
    rsNosExportados.Fields.Append "id", adVarChar, 255
    rsNosExportados.Open
End Sub

'Gera um vetor tempor�rio de n�s com seus atributos, como o objetivo de facilitar a leitura dos dados dos n�s da rede
'Cria uma c�pia da query da tabela watercomponents + points para RsNosTMP com todos os nos das tabelas relacionadas
'
'arquivoLog - nome do arquivo de logo onde est� sendo exportado o log do Epanet
'
Function CarregaRsNosTMP()

On Error GoTo Trata_Erro
    Dim layer_id As Long
    Dim strSQL As String
    
    layer_id = GetLayerID("WATERCOMPONENTS")
   
    'Gera a query desnormatizada junto aos nos(Watercomponents) para facilitar a leitura dos dados dos mesmos
    'Select a.OBJECT_ID_, X, Y, ID_TYPE, GROUNDHEIGHT, DEMAND, Pattern, SubTypeValve,
    'case when State = 2 then 'Closed' else 'Open' end state FROM (Select OBJECT_ID_, X, Y, ID_TYPE,
    'GROUNDHEIGHT, DEMAND, Pattern FROM watercomponents inner join points2 on object_id_=object_id)
    ' a Left Join (select object_id_,value_ as SubTypeValve from watercomponentsdata  where id_type = 1
    'and id_subtype = 1) b on a.object_id_=b.object_id_  left Join (select object_id_,value_ as State
    'from watercomponentsdata  where id_type = 1 and id_subtype = 2) c on a.object_id_=c.object_id_

    ' * Alguns n�meros acima s�o vari�veis na query a seguir
    'Exemplo de resultado da query:
    'OBJECT_ID_; X; Y; TIPO DE COMPONENTE; COTA; DEMANDA DE CONSUMO;PADR�O;ESTADO
    '100     289716,2251315639   9110857,324804159   25  0,  0,  0       NULL    Open
    '10000   291963,3551800701   9110854,729955614   0   0,  0,  NULL    NULL    Open
    '10001   291975,6117865313   9110853,035953095   0   0,  0,  NULL    NULL    Open
    '10002   291986,8719209225   9110851,24230337    0   0,  0,  NULL    NULL    Open
    '10003   291991,2563980305   9110857,021841375   0   0,  0,  NULL    NULL    Open

    strSQL = " Select a.OBJECT_ID_"
    strSQL = strSQL & ", x, y, ID_TYPE, GROUNDHEIGHT, DEMAND, Pattern, SubTypeValve, case when State = 2 then 'Closed' else 'Open' end state"
    strSQL = strSQL & " FROM "
    strSQL = strSQL & "(Select OBJECT_ID_"
    strSQL = strSQL & ", X, Y, ID_TYPE, GROUNDHEIGHT, DEMAND, Pattern"
    strSQL = strSQL & " FROM watercomponents inner join points" & layer_id & " on object_id_=object_id) a"
    strSQL = strSQL & " Left Join"
    strSQL = strSQL & " (select object_id_,value_ as SubTypeValve from watercomponentsdata  where id_type = 1 and id_subtype = 1) b"
    strSQL = strSQL & " on a.object_id_=b.object_id_"
    strSQL = strSQL & "  left Join (select object_id_,value_ as State from watercomponentsdata  where id_type = 1 and id_subtype = 2) c"
    strSQL = strSQL & " on a.object_id_=c.object_id_"

    Set rsNos = New ADODB.Recordset

    rsNos.Open strSQL, conn ', adOpenDynamic, adLockReadOnly

    While Not rsNos.EOF
        With rsNosTmp
          .AddNew
          .Fields("ID").Value = rsNos.Fields("OBJECT_ID_").Value
          .Fields("X").Value = rsNos.Fields("x").Value
          .Fields("Y").Value = rsNos.Fields("y").Value
          .Fields("Tipo").Value = IIf(IsNull(rsNos.Fields("id_type").Value), 0, rsNos.Fields("id_type").Value)
'          If rsNos.Fields("ID_TYPE").Value = No_Valvulas Then
'             Select Case rsNos.Fields("SubTypeValve").Value
'                Case 4, 0
'                   .Fields("Tipo").Value = 1
'                Case Else
'                   .Fields("Tipo").Value = 99
'             End Select
'          End If
            .Fields("Cota").Value = IIf(IsNull(rsNos.Fields("GROUNDHEIGHT").Value), 0, rsNos.Fields("GROUNDHEIGHT").Value)
            .Fields("Demanda").Value = IIf(IsNull(rsNos.Fields("demand").Value), 0, rsNos.Fields("demand").Value)
            .Fields("Padrao").Value = IIf(IsNull(rsNos.Fields("PATTERN").Value), 0, rsNos.Fields("PATTERN").Value)
            .Fields("estado").Value = rsNos.Fields("state").Value
       End With
       rsNos.MoveNext
    Wend

Trata_Erro:
    If Err.Number = 0 Or Err.Number = 20 Then
        Resume Next
    Else
        Close #2
        Open App.Path & "\LogErroExportEPANET.txt" For Append As #2
        Print #2, Now & "  - ModExporte - Sub CarregaRsNosTMP() - Linha: " & intLinhaCod & " - " & Err.Number & " - " & Err.Description
        Close #2
        MsgBox "Um posss�vel erro foi identificado na rotina 'CarregaRsNosTMP()':" & Chr(13) & Chr(13) & Err.Description & Chr(13) & Chr(13) & "Foi gerado na pasta do aplicativo o arquivo LogErroExportEPANET.txt com informa��es desta ocorrencia.", vbInformation
        If rsNos.EOF = False Then
            MsgBox "Problema com o n� de rede n�mero: " & rsNos.Fields("OBJECT_ID_").Value
        End If
        'Resume
    End If
End Function
