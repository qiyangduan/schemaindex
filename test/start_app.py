from notebook import notebookapp
NotebookApp = notebookapp.NotebookApp

if __name__ == '__main__':
    app = NotebookApp()
    app.initialize()
    app.default_url = '/schemaindex/overview'
    app.start()
