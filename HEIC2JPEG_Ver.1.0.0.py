import wx
import os
import PIL.Image
import pillow_heif

class HEICtoJPEGConverter(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 170))
        self.Center()

        # パネルの作成
        panel = wx.Panel(self)

        # 入力フォルダ選択用のボタン
        input_folder_button = wx.Button(panel, label="･･･")
        input_folder_button.Bind(wx.EVT_BUTTON, self.on_input_folder_button)

        # 入力フォルダパスを表示するテキストボックス
        self.input_folder_text = wx.TextCtrl(panel, style=wx.TE_READONLY)

        # 出力フォルダ選択用のボタン
        output_folder_button = wx.Button(panel, label="･･･")
        output_folder_button.Bind(wx.EVT_BUTTON, self.on_output_folder_button)

        # 出力フォルダパスを表示するテキストボックス
        self.output_folder_text = wx.TextCtrl(panel, style=wx.TE_READONLY)

        # 変換ボタン
        convert_button = wx.Button(panel, label="Convert")
        convert_button.Bind(wx.EVT_BUTTON, self.on_convert_button)

        # ラベルの作成
        input_folder_label = wx.StaticText(panel, label="入力フォルダ:")
        output_folder_label = wx.StaticText(panel, label="出力フォルダ:")

        # レイアウト
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 入力フォルダ部分
        input_folder_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_folder_sizer.Add(input_folder_label, 0, wx.ALL | wx.EXPAND, 5)
        input_folder_sizer.Add(self.input_folder_text, 1, wx.ALL | wx.EXPAND, 5)
        input_folder_sizer.Add(input_folder_button, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(input_folder_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # 出力フォルダ部分
        output_folder_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_folder_sizer.Add(output_folder_label, 0, wx.ALL | wx.EXPAND, 5)
        output_folder_sizer.Add(self.output_folder_text, 1, wx.ALL | wx.EXPAND, 5)
        output_folder_sizer.Add(output_folder_button, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(output_folder_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # 変換ボタン
        sizer.Add(convert_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        panel.SetSizer(sizer)

    def on_input_folder_button(self, event):
        """入力フォルダ選択ダイアログを表示"""
        dlg = wx.DirDialog(self, "入力フォルダを選択", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.input_folder = dlg.GetPath()
            self.input_folder_text.SetValue(self.input_folder)

    def on_output_folder_button(self, event):
        """出力フォルダ選択ダイアログを表示"""
        dlg = wx.DirDialog(self, "出力フォルダを選択", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.output_folder = dlg.GetPath()
            self.output_folder_text.SetValue(self.output_folder)

    def on_convert_button(self, event):
        """HEICファイルをJPEGに変換"""
        if not self.input_folder or not self.output_folder:
            wx.MessageBox("入力フォルダと出力フォルダを指定してください。", "エラー", wx.OK | wx.ICON_ERROR)
            return

        for filename in os.listdir(self.input_folder):
            if filename.endswith(".HEIC") or filename.endswith(".heic"):
                input_path = os.path.join(self.input_folder, filename)
                output_path = os.path.join(self.output_folder, os.path.splitext(filename)[0] + ".jpg")

                # HEICファイルをJPGに変換
                heif_file = pillow_heif.read_heif(input_path)
                image = PIL.Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
                image.save(output_path, 'JPEG')

                print(f'{input_path} を {output_path} に変換しました。')

        wx.MessageBox("変換が完了しました。", "完了", wx.OK | wx.ICON_INFORMATION)

if __name__ == "__main__":
    app = wx.App()
    frame = HEICtoJPEGConverter(None, "HEIC to JPEG Converter")
    frame.Show()
    app.MainLoop()
