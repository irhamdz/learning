from flask_restful import Resource
from flask import request

from flask_send_mail.models import Recipient, RecipientSchema, db, EventEmail


class RecipientListResource(Resource):
    def get(self):
        """
        func to response to a request GET /api/recipients with the complete list of recipients
        :return: sorted list of recipients, 200 OK
        """
        recipient = Recipient.query.all()
        recipient_schema = RecipientSchema(many=True)
        return recipient_schema.dump(recipient)

    def post(self):
        """
        func to response a request POST /api/recipients
        :return: detail recipient, 201 created
        """

        new_recipient = Recipient(
            name=request.json['name'],
            email=request.json['email'],
        )

        db.session.add(new_recipient)
        db.session.commit()
        recipient_schema = RecipientSchema()
        return recipient_schema.dump(new_recipient), 201


class RecipientResource(Resource):
    def get(self, id):
        """
        func to response to a request GET /api/recipients/{id}
        :return: detail of event email given id, 200 OK, or 404 NOT FOUND
        """
        recipient = Recipient.query.get_or_404(id, description=f"Recipient with id {id} not found")
        recipient_schema = RecipientSchema()
        return recipient_schema.dump(recipient)

    def patch(self, id):
        """
        func to response to a request PATCH /api/recipients/{id}
        :return: detail of event email given id, 200 OK, or 404 NOT FOUND
        """
        recipient = Recipient.query.get_or_404(id, description=f"Recipient with id {id} not found")
        recipient_schema = RecipientSchema()

        if 'name' in request.json:
            recipient.name = request.json['name']
        if 'email' in request.json:
            recipient.email = request.json['email']

        db.session.commit()
        return recipient_schema.dump(recipient)

    def delete(self, id):
        """
        func to response to a request DELETE /api/recipients/{id}
        :return: 204 No Content
        """
        recipient = Recipient.query.get_or_404(id)
        db.session.delete(recipient)
        db.session.commit()
        return '', 204
