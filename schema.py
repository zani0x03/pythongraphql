import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    employees = SQLAlchemyConnectionField(Employee.connection)
    # Disable sorting over this field
    #all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)
    departments = graphene.List(lambda:Department, name = graphene.String())

    def resolve_departments(self, info, name=None):
        query = Department.get_query(info)
        if name:
            query = query.filter(DepartmentModel.name == name)
        return query.all()

schema = graphene.Schema(query=Query)