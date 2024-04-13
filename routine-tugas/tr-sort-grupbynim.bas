Sub SortCells()
    Dim ws As Worksheet
    Dim rng As Range
    Dim col As Integer
    Dim i As Integer
    Dim sheetsArray As Variant
    sheetsArray = Array("GAN-L", "GAN-P", "MUL")

    For Each ws In ThisWorkbook.Worksheets
        If Not IsError(Application.Match(ws.Name, sheetsArray, 0)) Then
            For i = 1 To 3
                Select Case i
                    Case 1
                        col = 4 ' Column D
                    Case 2
                        col = 9 ' Column I
                    Case 3
                        col = 14 ' Column N
                End Select
                For Each rng In ws.Columns(col).Cells
                    If Len(rng.Value) = 3 Then
                        ' Sort rows from the row of the found cell + 5 to the row of the found cell + 19 by the column to the left of the found cell
                        ws.Range(ws.Cells(rng.Row + 4, col - 1), ws.Cells(rng.Row + 18, col + 1)).Sort Key1:=ws.Cells(rng.Row + 5, col - 1), Order1:=xlAscending, Header:=xlGuess, OrderCustom:=1, MatchCase:=False, Orientation:=xlTopToBottom, DataOption1:=xlSortNormal
                    End If
                Next rng
            Next i
        End If
    Next ws
End Sub
