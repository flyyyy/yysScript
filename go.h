#ifndef GO_H
#define GO_H

#include <QDialog>

namespace Ui {
class go;
}

class go : public QDialog
{
    Q_OBJECT

public:
    explicit go(QWidget *parent = nullptr);
    ~go();

private:
    Ui::go *ui;
};

#endif // GO_H
