#include "go.h"
#include "ui_go.h"

go::go(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::go)
{
    ui->setupUi(this);
}

go::~go()
{
    delete ui;
}
